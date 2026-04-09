"use client"

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { harmonicData, thdData } from "@/lib/mock-data"

function ThdTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ value: number }>; label?: string }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-md border border-border bg-popover px-3 py-2 shadow-lg">
      <p className="mb-1 text-xs text-muted-foreground">{label}</p>
      <p className="text-sm font-medium text-chart-3">
        THD: {payload[0].value.toFixed(2)}%
      </p>
    </div>
  )
}

function HarmonicTooltip({ active, payload }: { active?: boolean; payload?: Array<{ value: number; payload: { label: string } }> }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-md border border-border bg-popover px-3 py-2 shadow-lg">
      <p className="mb-1 text-xs text-muted-foreground">{payload[0].payload.label}</p>
      <p className="text-sm font-medium text-chart-2">
        Magnitude: {payload[0].value}%
      </p>
    </div>
  )
}

export function HarmonicAnalysis() {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {/* THD Over Time */}
      <Card className="border-border bg-card">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-foreground">Total Harmonic Distortion (THD)</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={thdData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="time" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
              <YAxis tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} unit="%" />
              <Tooltip content={<ThdTooltip />} />
              <Line type="monotone" dataKey="thd" stroke="var(--chart-3)" strokeWidth={2} dot={false} name="THD" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Harmonic Components */}
      <Card className="border-border bg-card">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-foreground">Harmonic Components</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={harmonicData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="harmonic" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} unit="%" />
              <Tooltip content={<HarmonicTooltip />} />
              <Bar dataKey="magnitude" radius={[4, 4, 0, 0]} name="Magnitude">
                {harmonicData.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={index === 0 ? "var(--chart-1)" : "var(--chart-2)"}
                    opacity={index === 0 ? 1 : 0.6 + index * 0.05}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
