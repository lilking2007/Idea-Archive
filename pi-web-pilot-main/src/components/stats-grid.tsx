import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { 
  Globe, 
  Activity, 
  FileText, 
  Clock,
  TrendingUp,
  Zap
} from "lucide-react";

const stats = [
  {
    title: "Active Projects",
    value: "12",
    icon: Globe,
    change: "+2 this week",
    trend: "up"
  },
  {
    title: "Total Deployments", 
    value: "47",
    icon: Zap,
    change: "+8 this month", 
    trend: "up"
  },
  {
    title: "Files Managed",
    value: "1,247",
    icon: FileText,
    change: "+156 files",
    trend: "up"
  },
  {
    title: "Uptime",
    value: "99.9%",
    icon: Activity,
    change: "30 days",
    trend: "stable"
  }
];

export const StatsGrid = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <Card key={stat.title} className="bg-gradient-card border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {stat.title}
            </CardTitle>
            <stat.icon className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <TrendingUp className="h-3 w-3 mr-1 text-status-live" />
              {stat.change}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};