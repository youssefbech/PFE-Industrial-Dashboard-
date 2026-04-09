"use client"

import { useState } from "react"
import Link from "next/link"
import {
  Activity,
  BarChart3,
  Bell,
  ChevronLeft,
  ChevronRight,
  Cpu,
  Gauge,
  LayoutDashboard,
  Radio,
  Settings,
  Waves,
  Zap,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { ScrollArea } from "@/components/ui/scroll-area"

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "#", active: true },
  { icon: Zap, label: "Electrical", href: "#" },
  { icon: Cpu, label: "AI Engine", href: "#" },
  { icon: Waves, label: "Harmonics", href: "#" },
  { icon: Bell, label: "Alerts", href: "#" },
  { icon: Gauge, label: "Machines", href: "#" },
  { icon: BarChart3, label: "Analytics", href: "#" },
  { icon: Settings, label: "Settings", href: "#" },
]

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <TooltipProvider delayDuration={0}>
      <aside
        className={cn(
          "flex h-screen flex-col border-r border-border bg-sidebar transition-all duration-300",
          collapsed ? "w-16" : "w-56"
        )}
      >
        {/* Logo */}
        <div className="flex h-14 items-center gap-2 border-b border-border px-4">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-primary">
            <Radio className="h-4 w-4 text-primary-foreground" />
          </div>
          {!collapsed && (
            <div className="flex flex-col overflow-hidden">
              <span className="truncate text-sm font-semibold text-sidebar-foreground">Edge AI</span>
              <span className="truncate text-xs text-muted-foreground">IoT Gateway</span>
            </div>
          )}
        </div>

        {/* Nav Items */}
        <ScrollArea className="flex-1 py-3">
          <nav className="flex flex-col gap-1 px-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const button = (
                <Link
                  key={item.label}
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                    item.active
                      ? "bg-sidebar-accent text-primary"
                      : "text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-foreground"
                  )}
                >
                  <Icon className="h-4 w-4 shrink-0" />
                  {!collapsed && <span className="truncate">{item.label}</span>}
                </Link>
              )

              if (collapsed) {
                return (
                  <Tooltip key={item.label}>
                    <TooltipTrigger asChild>{button}</TooltipTrigger>
                    <TooltipContent side="right" className="bg-popover text-popover-foreground">
                      {item.label}
                    </TooltipContent>
                  </Tooltip>
                )
              }

              return button
            })}
          </nav>
        </ScrollArea>

        {/* Status indicator */}
        <div className="border-t border-border px-3 py-3">
          {!collapsed && (
            <div className="mb-2 flex items-center gap-2 rounded-md bg-secondary px-3 py-2">
              <Activity className="h-3 w-3 text-primary" />
              <span className="text-xs text-muted-foreground">System Online</span>
            </div>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setCollapsed(!collapsed)}
            className="w-full justify-center text-muted-foreground hover:text-foreground"
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </Button>
        </div>
      </aside>
    </TooltipProvider>
  )
}
