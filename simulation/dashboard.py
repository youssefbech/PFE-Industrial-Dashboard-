import streamlit as st
import paho.mqtt.client as mqtt
import json
import pandas as pd
import queue
import time
from datetime import datetime

# 1. CONFIGURATION
st.set_page_config(page_title="Core-AI Industrial", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stMetric"] {
        background-color: #161b22; border: 1px solid #30363d;
        padding: 15px; border-radius: 12px; transition: transform 0.2s;
    }
    [data-testid="stMetric"]:hover { transform: translateY(-5px); border-color: #58a6ff; }
    h1, h2, h3 { color: #f0f6fc; font-weight: 600 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 4px 4px 0px 0px; padding: 8px 16px; }
    </style>
    """, unsafe_allow_html=True)

if 'motors_data' not in st.session_state:
    st.session_state.motors_data = {}

# Mapping des types d'anomalies
FAULT_TYPES = {
    1: ("Surcharge (courant élevé)", "Électrique", "#ff9500"),
    2: ("Chute de tension", "Électrique", "#ff9500"),
    3: ("Surchauffe", "Thermique", "#ff4b4b"),
    4: ("Instabilité (ΔV élevé + variations)", "Électrique + Thermique", "#ff2d55")
}

# 2. RECEPTION MQTT
def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        motor_id = topic_parts[1].upper()
        payload = json.loads(msg.payload.decode('utf-8'))
        payload['motor_id'] = motor_id
        userdata.put(payload)
    except Exception as e:
        print(f"❌ Erreur dashboard on_message : {e}")

@st.cache_resource
def init_mqtt():
    q = queue.Queue()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=q)
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("motor/+/data")
    client.loop_start()
    return client, q

mqtt_client, data_queue = init_mqtt()

# Lecture de tous les messages disponibles dans la queue
while not data_queue.empty():
    msg = data_queue.get()
    m_id = msg['motor_id']
    msg['Time'] = datetime.now().strftime("%H:%M:%S")

    if m_id not in st.session_state.motors_data:
        st.session_state.motors_data[m_id] = []

    st.session_state.motors_data[m_id].append(msg)

    if len(st.session_state.motors_data[m_id]) > 60:
        st.session_state.motors_data[m_id].pop(0)

# 3. SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🏭 FLOTTE IA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.motors_data:
        motor_list = sorted(list(st.session_state.motors_data.keys()))
        selected_motor = st.selectbox("🎯 Sélection de l'unité", motor_list)
        
        st.write("🔧 **Vue rapide :**")
        for m in motor_list:
            last_v = st.session_state.motors_data[m][-1]
            fault_label = int(last_v.get('fault_label', last_v.get('anomaly_score', 0)))
            is_err = fault_label != 0
            icon = "🔴" if is_err else "🟢"
            if is_err:
                fault_name = FAULT_TYPES.get(fault_label, ("Anomalie", "", "#ff4b4b"))[0]
                st.caption(f"{icon} **{m}** - {fault_name}")
            else:
                st.caption(f"{icon} {m}")
    else:
        st.info("Recherche de signaux MQTT...")
        selected_motor = None

# 4. INTERFACE PRINCIPALE
if selected_motor:
    df = pd.DataFrame(st.session_state.motors_data[selected_motor])
    last = df.iloc[-1]
    is_anomaly = int(last.get('anomaly_score', 0)) != 0

    head_col, status_col = st.columns([4, 1])
    with head_col:
        st.title(f"Machine : {selected_motor}")
    with status_col:
        if is_anomaly:
            fault_label = int(last.get('fault_label', last.get('anomaly_score', 0)))
            fault_info = FAULT_TYPES.get(fault_label, ("Anomalie inconnue", "Inconnu", "#ff4b4b"))
            fault_name, fault_cat, fault_color = fault_info
            
            st.markdown(f"""
                <div style='background-color:#6e1d1d; padding:10px; border-radius:8px; text-align:center; 
                color:white; font-weight:bold; border:2px solid #ff4b4b; margin-bottom:5px;'>
                    ⚠️ ANOMALIE
                </div>
                <div style='background-color:{fault_color}33; padding:8px; border-radius:6px; 
                text-align:center; color:{fault_color}; font-size:12px; border:1px solid {fault_color};'>
                    <b>{fault_name}</b><br>
                    <span style='font-size:10px; opacity:0.8;'>{fault_cat}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color:#1d3d24; padding:10px; border-radius:8px; text-align:center; color:white; font-weight:bold; border:1px solid #28a745;'>✅ NOMINAL</div>", unsafe_allow_html=True)

    st.write("### ⚡ Paramètres Temps Réel")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Puissance", f"{last['power']:.1f} W", delta=f"{last['power']-df['power'].mean():.1f}")
    m2.metric("Courant", f"{last['current']:.2f} A")
    m3.metric("Tension", f"{last['voltage']:.1f} V")
    m4.metric("Température", f"{last['temp']:.1f} °C", delta_color="inverse")

    st.markdown("---")

    tab_charts, tab_data = st.tabs(["📊 Analyses Graphiques", "📋 Registre de Données"])

    with tab_charts:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Consommation Électrique")
            st.line_chart(df.set_index('Time')[['voltage', 'current']], color=["#3498db", "#e67e22"])
        with c2:
            st.subheader("Profil Thermique")
            t_color = "#ff4b4b" if is_anomaly else "#2ecc71"
            st.area_chart(df.set_index('Time')['temp'], color=t_color)

    with tab_data:
        st.dataframe(df.sort_index(ascending=False), use_container_width=True, height=300)
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger les logs", csv_export, f"logs_{selected_motor}.csv", "text/csv")

# 5. RAFRAÎCHISSEMENT
time.sleep(1)
st.rerun()