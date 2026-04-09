"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Thermometer, RotateCw, Weight } from "lucide-react"
import { machines } from "@/lib/mock-data"

const statusConfig = {
  normal: { label: "Normal", dotClass: "bg-primary", badgeClass: "border-primary/30 bg-primary/10 text-primary" },
  warning: { label: "Warning", dotClass: "bg-warning", badgeClass: "border-warning/30 bg-warning/10 text-warning" },
  critical: { label: "Critical", dotClass: "bg-destructive", badgeClass: "border-destructive/30 bg-destructive/10 text-destructive" },
}

export function MachineStatus() {
  return (
    <Card className="border-border bg-card">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-foreground">Machine Status Overview</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {machines.map((machine) => {
            const config = statusConfig[machine.status]
            return (
              <div
                key={machine.id}
                className="rounded-lg border border-border bg-secondary/50 p-3 transition-colors hover:bg-secondary"
              >
                <div className="mb-2 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={`h-2.5 w-2.5 rounded-full ${config.dotClass}`} />
                    <span className="font-mono text-xs font-medium text-foreground">{machine.id}</span>
                  </div>
                  <Badge variant="outline" className={`text-[10px] ${config.badgeClass}`}>
                    {config.label}
                  </Badge>
                </div>
                <p className="mb-3 truncate text-xs text-muted-foreground">{machine.name}</p>

                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2">
                    <Thermometer className="h-3 w-3 shrink-0 text-muted-foreground" />
                    <div className="flex flex-1 items-center gap-2">
                      <Progress
                        value={machine.temp}
                        className="h-1.5 bg-secondary [&>div]:bg-chart-4"
                      />
                      <span className="w-10 text-right font-mono text-[10px] text-muted-foreground">{machine.temp}°C</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <RotateCw className="h-3 w-3 shrink-0 text-muted-foreground" />
                    <span className="font-mono text-[10px] text-muted-foreground">{machine.rpm} RPM</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Weight className="h-3 w-3 shrink-0 text-muted-foreground" />
                    <div className="flex flex-1 items-center gap-2">
                      <Progress
                        value={machine.load}
                        className="h-1.5 bg-secondary [&>div]:bg-chart-2"
                      />
                      <span className="w-10 text-right font-mono text-[10px] text-muted-foreground">{machine.load}%</span>
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
