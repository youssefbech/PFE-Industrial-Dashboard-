"use client"

import { Activity, AlertTriangle, Clock, Shield } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { kpiData } from "@/lib/mock-data"

const kpis = [
  {
    label: "System Uptime",
    value: `${kpiData.uptime}%`,
    icon: Clock,
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    label: "Anomalies Detected",
    value: kpiData.anomaliesDetected.toString(),
    icon: AlertTriangle,
    color: "text-warning",
    bgColor: "bg-warning/10",
  },
  {
    label: "Active Alerts",
    value: kpiData.activeAlerts.toString(),
    icon: Activity,
    color: "text-destructive",
    bgColor: "bg-destructive/10",
  },
  {
    label: "Model Accuracy",
    value: `${kpiData.modelAccuracy}%`,
    icon: Shield,
    color: "text-chart-2",
    bgColor: "bg-chart-2/10",
  },
]

export function KpiWidgets() {
  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      {kpis.map((kpi) => {
        const Icon = kpi.icon
        return (
          <Card key={kpi.label} className="border-border bg-card">
            <CardContent className="flex items-center gap-4 p-4">
              <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${kpi.bgColor}`}>
                <Icon className={`h-5 w-5 ${kpi.color}`} />
              </div>
              <div className="min-w-0">
                <p className="text-2xl font-bold text-foreground">{kpi.value}</p>
                <p className="truncate text-xs text-muted-foreground">{kpi.label}</p>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
