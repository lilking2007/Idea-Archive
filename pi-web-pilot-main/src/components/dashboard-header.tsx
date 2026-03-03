import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Plus, 
  Server, 
  Cpu, 
  HardDrive,
  Wifi
} from "lucide-react";
import logoImage from "@/assets/logo.png";

export const DashboardHeader = () => {
  return (
    <div className="border-b border-border/50 bg-gradient-hero">
      <div className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <img src={logoImage} alt="DeployPilot" className="h-8 w-8" />
              <div>
                <h1 className="text-2xl font-bold">DeployPilot</h1>
                <p className="text-sm text-muted-foreground">
                  Raspberry Pi Deployment Control Panel
                </p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-6 text-sm">
              <div className="flex items-center gap-2">
                <Server className="h-4 w-4 text-status-live" />
                <span className="text-muted-foreground">Pi Status:</span>
                <Badge variant="secondary" className="bg-status-live/10 text-status-live">
                  Online
                </Badge>
              </div>
              
              <div className="flex items-center gap-4 text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Cpu className="h-3 w-3" />
                  <span className="text-xs">45%</span>
                </div>
                <div className="flex items-center gap-1">
                  <HardDrive className="h-3 w-3" />
                  <span className="text-xs">12GB</span>
                </div>
                <div className="flex items-center gap-1">
                  <Wifi className="h-3 w-3" />
                  <span className="text-xs">Good</span>
                </div>
              </div>
            </div>
            
            <Button className="bg-gradient-primary shadow-primary">
              <Plus className="h-4 w-4 mr-2" />
              New Project
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};