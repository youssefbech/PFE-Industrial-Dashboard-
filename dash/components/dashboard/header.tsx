"use client"

import { Bell, Search, Wifi } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function Header() {
  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-card px-6">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold text-foreground">
          Industrial Edge AI IoT Gateway
        </h1>
        <Badge variant="outline" className="border-primary/30 bg-primary/10 text-primary">
          <Wifi className="mr-1 h-3 w-3" />
          Live
        </Badge>
      </div>

      <div className="flex items-center gap-3">
        <div className="relative hidden md:block">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search machines..."
            className="w-64 bg-secondary pl-9 text-sm text-foreground placeholder:text-muted-foreground"
          />
        </div>
        <Button variant="ghost" size="icon" className="relative text-muted-foreground hover:text-foreground">
          <Bell className="h-4 w-4" />
          <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-destructive text-[10px] font-bold text-destructive-foreground">
            4
          </span>
          <span className="sr-only">Notifications</span>
        </Button>
        <div className="flex items-center gap-2 rounded-md bg-secondary px-3 py-1.5">
          <div className="h-2 w-2 rounded-full bg-primary" />
          <span className="text-xs font-medium text-foreground">Operator</span>
        </div>
      </div>
    </header>
  )
}
