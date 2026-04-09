// Generate realistic electrical monitoring time-series data
function generateTimeSeriesData(points: number, baseTime: Date) {
  const data = []
  for (let i = 0; i < points; i++) {
    const time = new Date(baseTime.getTime() - (points - i) * 5000)
    const noise = () => (Math.random() - 0.5) * 2

    data.push({
      time: time.toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" }),
      voltage: 220 + Math.sin(i * 0.1) * 8 + noise() * 3,
      current: 15 + Math.sin(i * 0.15 + 1) * 3 + noise() * 0.8,
      power: 3.3 + Math.sin(i * 0.12 + 2) * 0.6 + noise() * 0.15,
    })
  }
  return data
}

function generateAnomalyData(points: number, baseTime: Date) {
  const data = []
  for (let i = 0; i < points; i++) {
    const time = new Date(baseTime.getTime() - (points - i) * 10000)
    let score = 0.1 + Math.random() * 0.15

    // Create some anomaly spikes
    if (i === 18 || i === 19) score = 0.72 + Math.random() * 0.15
    if (i === 35) score = 0.85 + Math.random() * 0.1
    if (i === 52 || i === 53) score = 0.68 + Math.random() * 0.12

    data.push({
      time: time.toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit" }),
      score: parseFloat(score.toFixed(3)),
      threshold: 0.6,
    })
  }
  return data
}

const baseTime = new Date()

export const electricalData = generateTimeSeriesData(60, baseTime)

export const anomalyData = generateAnomalyData(60, baseTime)

export const harmonicData = [
  { harmonic: "H1", magnitude: 100, label: "Fundamental" },
  { harmonic: "H3", magnitude: 12.5, label: "3rd Harmonic" },
  { harmonic: "H5", magnitude: 8.2, label: "5th Harmonic" },
  { harmonic: "H7", magnitude: 4.7, label: "7th Harmonic" },
  { harmonic: "H9", magnitude: 2.1, label: "9th Harmonic" },
  { harmonic: "H11", magnitude: 1.3, label: "11th Harmonic" },
]

export const thdData = Array.from({ length: 30 }, (_, i) => {
  const time = new Date(baseTime.getTime() - (30 - i) * 60000)
  return {
    time: time.toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit" }),
    thd: 5.2 + Math.sin(i * 0.3) * 1.5 + (Math.random() - 0.5) * 0.8,
  }
})

export const events = [
  { id: 1, timestamp: "2026-03-05 14:32:18", type: "Anomaly Detected", severity: "critical" as const, machineId: "MTR-003", description: "Bearing vibration anomaly detected - immediate inspection required" },
  { id: 2, timestamp: "2026-03-05 14:28:05", type: "Threshold Alert", severity: "warning" as const, machineId: "MTR-007", description: "Current draw exceeded 18A threshold for 30 seconds" },
  { id: 3, timestamp: "2026-03-05 14:15:42", type: "Anomaly Detected", severity: "warning" as const, machineId: "MTR-001", description: "Unusual harmonic pattern in power spectrum" },
  { id: 4, timestamp: "2026-03-05 13:58:11", type: "System Event", severity: "info" as const, machineId: "GW-001", description: "Edge AI model updated to v2.4.1 - inference latency improved" },
  { id: 5, timestamp: "2026-03-05 13:45:30", type: "Threshold Alert", severity: "critical" as const, machineId: "MTR-005", description: "Temperature sensor reading above 85C - cooling system check" },
  { id: 6, timestamp: "2026-03-05 13:30:22", type: "Recovery", severity: "info" as const, machineId: "MTR-002", description: "Motor parameters returned to normal operating range" },
  { id: 7, timestamp: "2026-03-05 13:12:08", type: "Anomaly Detected", severity: "warning" as const, machineId: "MTR-004", description: "Phase imbalance detected - voltage asymmetry at 3.2%" },
  { id: 8, timestamp: "2026-03-05 12:55:44", type: "System Event", severity: "info" as const, machineId: "GW-001", description: "Scheduled data sync completed - 2,847 records transmitted" },
]

export const machines = [
  { id: "MTR-001", name: "Conveyor Motor A", status: "normal" as const, temp: 62, rpm: 1480, load: 72 },
  { id: "MTR-002", name: "Pump Motor B", status: "normal" as const, temp: 58, rpm: 2960, load: 65 },
  { id: "MTR-003", name: "Compressor C", status: "critical" as const, temp: 87, rpm: 1475, load: 95 },
  { id: "MTR-004", name: "Fan Motor D", status: "warning" as const, temp: 71, rpm: 1490, load: 81 },
  { id: "MTR-005", name: "Mixer Motor E", status: "critical" as const, temp: 86, rpm: 740, load: 92 },
  { id: "MTR-006", name: "Conveyor Motor F", status: "normal" as const, temp: 55, rpm: 1478, load: 60 },
  { id: "MTR-007", name: "Hydraulic Pump G", status: "warning" as const, temp: 74, rpm: 2955, load: 88 },
  { id: "MTR-008", name: "Extruder Motor H", status: "normal" as const, temp: 64, rpm: 1482, load: 70 },
]

export const kpiData = {
  uptime: 99.7,
  anomaliesDetected: 23,
  activeAlerts: 4,
  modelAccuracy: 97.2,
}

export const aiPrediction = {
  anomalyScore: 0.23,
  modelStatus: "Active" as const,
  confidence: 97.2,
  lastInference: "2s ago",
  modelVersion: "v2.4.1",
}
