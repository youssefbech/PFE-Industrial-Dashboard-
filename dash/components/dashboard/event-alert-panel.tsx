"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { events } from "@/lib/mock-data"

function SeverityBadge({ severity }: { severity: "critical" | "warning" | "info" }) {
  const config = {
    critical: "border-destructive/30 bg-destructive/10 text-destructive",
    warning: "border-warning/30 bg-warning/10 text-warning",
    info: "border-chart-2/30 bg-chart-2/10 text-chart-2",
  }

  return (
    <Badge variant="outline" className={`text-xs ${config[severity]}`}>
      {severity.charAt(0).toUpperCase() + severity.slice(1)}
    </Badge>
  )
}

export function EventAlertPanel() {
  return (
    <Card className="border-border bg-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-foreground">Event & Alert Log</CardTitle>
        <Badge variant="outline" className="border-destructive/30 bg-destructive/10 text-xs text-destructive">
          4 Active
        </Badge>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[320px]">
          <Table>
            <TableHeader>
              <TableRow className="border-border hover:bg-transparent">
                <TableHead className="text-xs text-muted-foreground">Timestamp</TableHead>
                <TableHead className="text-xs text-muted-foreground">Event</TableHead>
                <TableHead className="text-xs text-muted-foreground">Severity</TableHead>
                <TableHead className="text-xs text-muted-foreground">Machine</TableHead>
                <TableHead className="hidden text-xs text-muted-foreground md:table-cell">Description</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {events.map((event) => (
                <TableRow key={event.id} className="border-border hover:bg-secondary/50">
                  <TableCell className="py-2.5 font-mono text-xs text-muted-foreground">
                    {event.timestamp.split(" ")[1]}
                  </TableCell>
                  <TableCell className="py-2.5 text-xs text-foreground">{event.type}</TableCell>
                  <TableCell className="py-2.5">
                    <SeverityBadge severity={event.severity} />
                  </TableCell>
                  <TableCell className="py-2.5 font-mono text-xs text-foreground">{event.machineId}</TableCell>
                  <TableCell className="hidden max-w-[300px] truncate py-2.5 text-xs text-muted-foreground md:table-cell">
                    {event.description}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
