"use client"

import { useEffect, useState } from "react"
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Brain, Cpu, ShieldCheck, Timer } from "lucide-react"
import { anomalyData as initialAnomalyData, aiPrediction } from "@/lib/mock-data"

function CustomTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ value: number; name: string }>; label?: string }) {
  if (!active || !payload?.length) return null
  const score = payload[0]?.value ?? 0
  const isAnomaly = score > 0.6
  return (
    <div className="rounded-md border border-border bg-popover px-3 py-2 shadow-lg">
      <p className="mb-1 text-xs text-muted-foreground">{label}</p>
      <p className={`text-sm font-bold ${isAnomaly ? "text-destructive" : "text-primary"}`}>
        Score: {score.toFixed(3)}
      </p>
      {isAnomaly && <p className="text-xs font-medium text-destructive">Anomaly Detected</p>}
    </div>
  )
}

export function AnomalyDetection() {
  const [data, setData] = useState(initialAnomalyData)

  useEffect(() => {
    const interval = setInterval(() => {
      setData((prev) => {
        const newPoint = {
          time: new Date().toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit" }),
          score: parseFloat((0.1 + Math.random() * 0.2).toFixed(3)),
          threshold: 0.6,
        }
        return [...prev.slice(1), newPoint]
      })
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="grid gap-4 lg:grid-cols-3">
      {/* Anomaly Timeline */}
      <Card className="border-border bg-card lg:col-span-2">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-foreground">AI Anomaly Detection</CardTitle>
          <Badge variant="outline" className="border-chart-2/30 bg-chart-2/10 text-xs text-chart-2">
            <Brain className="mr-1 h-3 w-3" />
            Model Active
          </Badge>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={data}>
              <defs>
                <linearGradient id="anomalyGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="anomalyHighGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--destructive)" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="var(--destructive)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="time" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
              <YAxis tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} domain={[0, 1]} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0.6} stroke="var(--destructive)" strokeDasharray="6 3" strokeWidth={1.5} label={{ value: "Threshold", position: "right", fill: "var(--destructive)", fontSize: 10 }} />
              <Area
                type="monotone"
                dataKey="score"
                stroke="var(--chart-1)"
                strokeWidth={2}
                fill="url(#anomalyGradient)"
                dot={(props: { cx: number; cy: number; payload: { score: number } }) => {
                  if (props.payload.score > 0.6) {
                    return (
                      <circle
                        key={`dot-${props.cx}-${props.cy}`}
                        cx={props.cx}
                        cy={props.cy}
                        r={4}
                        fill="var(--destructive)"
                        stroke="var(--destructive)"
                        strokeWidth={2}
                      />
                    )
                  }
                  return <circle key={`dot-${props.cx}-${props.cy}`} r={0} cx={props.cx} cy={props.cy} />
                }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* AI Prediction Panel */}
      <Card className="border-border bg-card">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-foreground">AI Prediction</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <div className="flex items-center justify-between rounded-lg bg-secondary p-3">
            <div className="flex items-center gap-2">
              <Brain className="h-4 w-4 text-chart-2" />
              <span className="text-xs text-muted-foreground">Anomaly Score</span>
            </div>
            <span className="text-lg font-bold text-primary">{aiPrediction.anomalyScore}</span>
          </div>

          <div className="flex items-center justify-between rounded-lg bg-secondary p-3">
            <div className="flex items-center gap-2">
              <Cpu className="h-4 w-4 text-chart-2" />
              <span className="text-xs text-muted-foreground">Model Status</span>
            </div>
            <Badge variant="outline" className="border-primary/30 bg-primary/10 text-xs text-primary">
              {aiPrediction.modelStatus}
            </Badge>
          </div>

          <div className="flex items-center justify-between rounded-lg bg-secondary p-3">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-chart-2" />
              <span className="text-xs text-muted-foreground">Confidence</span>
            </div>
            <span className="text-lg font-bold text-foreground">{aiPrediction.confidence}%</span>
          </div>

          <div className="flex items-center justify-between rounded-lg bg-secondary p-3">
            <div className="flex items-center gap-2">
              <Timer className="h-4 w-4 text-chart-2" />
              <span className="text-xs text-muted-foreground">Last Inference</span>
            </div>
            <span className="text-sm font-medium text-foreground">{aiPrediction.lastInference}</span>
          </div>

          <div className="mt-auto rounded-lg border border-border p-3">
            <p className="text-xs text-muted-foreground">Model Version</p>
            <p className="font-mono text-sm font-medium text-foreground">{aiPrediction.modelVersion}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
