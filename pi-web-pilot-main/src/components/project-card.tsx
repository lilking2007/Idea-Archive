import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { StatusBadge } from "@/components/ui/status-badge";
import { Badge } from "@/components/ui/badge";
import { 
  ExternalLink, 
  FolderOpen, 
  Settings, 
  Upload,
  GitBranch,
  Calendar
} from "lucide-react";

interface ProjectCardProps {
  name: string;
  status: "live" | "development" | "offline";
  url: string;
  lastDeployed: string;
  version: string;
  framework?: string;
}

export const ProjectCard = ({ 
  name, 
  status, 
  url, 
  lastDeployed, 
  version,
  framework = "Static"
}: ProjectCardProps) => {
  return (
    <Card className="bg-gradient-card hover:shadow-card transition-all duration-300 border-border/50 hover:border-primary/20">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <CardTitle className="text-lg font-semibold">{name}</CardTitle>
            <div className="flex items-center gap-2">
              <StatusBadge status={status} />
              <Badge variant="secondary" className="text-xs">
                {framework}
              </Badge>
            </div>
          </div>
          <Button 
            variant="ghost" 
            size="sm"
            className="text-muted-foreground hover:text-primary"
          >
            <ExternalLink className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        <div className="text-sm text-muted-foreground space-y-1">
          <div className="flex items-center gap-2">
            <Calendar className="h-3 w-3" />
            <span>Last deployed: {lastDeployed}</span>
          </div>
          <div className="flex items-center gap-2">
            <GitBranch className="h-3 w-3" />
            <span>Version: {version}</span>
          </div>
        </div>
        
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="flex-1">
            <FolderOpen className="h-4 w-4 mr-2" />
            Files
          </Button>
          <Button variant="outline" size="sm" className="flex-1">
            <Upload className="h-4 w-4 mr-2" />
            Deploy
          </Button>
          <Button variant="outline" size="sm">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};