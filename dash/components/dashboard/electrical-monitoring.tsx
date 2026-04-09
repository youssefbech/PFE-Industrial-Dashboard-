"use client"

import { useEffect, useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"

function generatePoint(i: number) {
  const noise = () => (Math.random() - 0.5) * 2
  const time = new Date()
  return {
    time: time.toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" }),
    voltage: 220 + Math.sin(i * 0.1) * 8 + noise() * 3,
    current: 15 + Math.sin(i * 0.15 + 1) * 3 + noise() * 0.8,
    power: 3.3 + Math.sin(i * 0.12 + 2) * 0.6 + noise() * 0.15,
  }
}

function initData(count: number) {
  return Array.from({ length: count }, (_, i) => generatePoint(i))
}

function CustomTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ value: number; name: string; color: string }>; label?: string }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-md border border-border bg-popover px-3 py-2 shadow-lg">
      <p className="mb-1 text-xs text-muted-foreground">{label}</p>
      {payload.map((entry) => (
        <p key={entry.name} className="text-sm font-medium" style={{ color: entry.color }}>
          {entry.name}: {entry.value.toFixed(2)}
        </p>
      ))}
    </div>
  )
}

export function ElectricalMonitoring() {
  const [data, setData] = useState(() => initData(40))
  const [counter, setCounter] = useState(40)

  useEffect(() => {
    const interval = setInterval(() => {
      setCounter((prev) => prev + 1)
      setData((prev) => {
        const newData = [...prev.slice(1), generatePoint(counter)]
        return newData
      })
    }, 2000)
    return () => clearInterval(interval)
  }, [counter])

  return (
    <Card className="border-border bg-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-foreground">Real-Time Electrical Monitoring</CardTitle>
        <Badge variant="outline" className="border-primary/30 bg-primary/10 text-xs text-primary">
          Live
        </Badge>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="voltage" className="w-full">
          <TabsList className="mb-4 bg-secondary">
            <TabsTrigger value="voltage" className="text-xs data-[state=active]:bg-primary/20 data-[state=active]:text-primary">
              Voltage (V)
            </TabsTrigger>
            <TabsTrigger value="current" className="text-xs data-[state=active]:bg-primary/20 data-[state=active]:text-primary">
              Current (A)
            </TabsTrigger>
            <TabsTrigger value="power" className="text-xs data-[state=active]:bg-primary/20 data-[state=active]:text-primary">
              Power (kW)
            </TabsTrigger>
          </TabsList>

          <TabsContent value="voltage">
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="time" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
                <YAxis tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} domain={["auto", "auto"]} />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="voltage" stroke="var(--chart-1)" strokeWidth={2} dot={false} name="Voltage" />
              </LineChart>
            </ResponsiveContainer>
          </TabsContent>

          <TabsContent value="current">
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="time" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
                <YAxis tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} domain={["auto", "auto"]} />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="current" stroke="var(--chart-2)" strokeWidth={2} dot={false} name="Current" />
              </LineChart>
            </ResponsiveContainer>
          </TabsContent>

          <TabsContent value="power">
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="time" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
                <YAxis tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} domain={["auto", "auto"]} />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="power" stroke="var(--chart-3)" strokeWidth={2} dot={false} name="Power" />
              </LineChart>
            </ResponsiveContainer>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
