"use client"

import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KpiWidgets } from "@/components/dashboard/kpi-widgets"
import { ElectricalMonitoring } from "@/components/dashboard/electrical-monitoring"
import { AnomalyDetection } from "@/components/dashboard/anomaly-detection"
import { HarmonicAnalysis } from "@/components/dashboard/harmonic-analysis"
import { EventAlertPanel } from "@/components/dashboard/event-alert-panel"
import { MachineStatus } from "@/components/dashboard/machine-status"
import { ScrollArea } from "@/components/ui/scroll-area"

export default function DashboardPage() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <ScrollArea className="flex-1">
          <main className="flex flex-col gap-4 p-4 lg:p-6">
            {/* KPI Widgets */}
            <KpiWidgets />

            {/* Real-Time Electrical Monitoring */}
            <ElectricalMonitoring />

            {/* AI Anomaly Detection */}
            <AnomalyDetection />

            {/* Harmonic Analysis */}
            <HarmonicAnalysis />

            {/* Bottom Row: Events + Machine Status */}
            <div className="grid gap-4 xl:grid-cols-2">
              <EventAlertPanel />
              <MachineStatus />
            </div>
          </main>
        </ScrollArea>
      </div>
    </div>
  )
}
