import { DashboardHeader } from "@/components/dashboard-header";
import { StatsGrid } from "@/components/stats-grid";
import { ProjectCard } from "@/components/project-card";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Search, 
  Filter, 
  MoreVertical,
  Clock,
  AlertTriangle
} from "lucide-react";

// Mock data for demo
const projects = [
  {
    name: "Personal Portfolio",
    status: "live" as const,
    url: "portfolio.local",
    lastDeployed: "2 hours ago",
    version: "v1.2.3",
    framework: "React"
  },
  {
    name: "Blog Website", 
    status: "development" as const,
    url: "blog.local",
    lastDeployed: "1 day ago",
    version: "v0.8.1",
    framework: "Static"
  },
  {
    name: "Client Project",
    status: "live" as const, 
    url: "client.local",
    lastDeployed: "3 days ago",
    version: "v2.1.0",
    framework: "Vue"
  },
  {
    name: "Test Environment",
    status: "offline" as const,
    url: "test.local", 
    lastDeployed: "1 week ago",
    version: "v0.1.0",
    framework: "Static"
  }
];

const recentActivity = [
  { action: "Deployed", project: "Personal Portfolio", time: "2 hours ago" },
  { action: "File uploaded", project: "Blog Website", time: "5 hours ago" },
  { action: "Backup created", project: "Client Project", time: "1 day ago" },
  { action: "Project created", project: "Test Environment", time: "3 days ago" }
];

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      
      <div className="container mx-auto px-6 py-8 space-y-8">
        {/* Stats Overview */}
        <StatsGrid />
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Projects Section */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Projects</h2>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">
                  <Search className="h-4 w-4 mr-2" />
                  Search
                </Button>
                <Button variant="outline" size="sm">
                  <Filter className="h-4 w-4 mr-2" />
                  Filter
                </Button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {projects.map((project) => (
                <ProjectCard key={project.name} {...project} />
              ))}
            </div>
          </div>
          
          {/* Activity Sidebar */}
          <div className="space-y-6">
            {/* Recent Activity */}
            <Card className="bg-gradient-card border-border/50">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start gap-3 text-sm">
                    <div className="w-2 h-2 rounded-full bg-primary mt-2 flex-shrink-0" />
                    <div className="space-y-1">
                      <p className="text-foreground">
                        <span className="font-medium">{activity.action}</span> {activity.project}
                      </p>
                      <p className="text-muted-foreground text-xs">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
            
            {/* System Status */}
            <Card className="bg-gradient-card border-border/50">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  System Status
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Nginx Proxy Manager</span>
                  <Badge className="bg-status-live/10 text-status-live">Online</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">SSH Connection</span>
                  <Badge className="bg-status-live/10 text-status-live">Connected</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">File System</span>
                  <Badge className="bg-status-live/10 text-status-live">Available</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Auto Backups</span>
                  <Badge className="bg-status-development/10 text-status-development">Scheduled</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
