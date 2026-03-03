import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const statusBadgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      status: {
        live: "bg-status-live/10 text-status-live border border-status-live/20",
        development: "bg-status-development/10 text-status-development border border-status-development/20",
        offline: "bg-status-offline/10 text-status-offline border border-status-offline/20",
      },
    },
    defaultVariants: {
      status: "offline",
    },
  }
);

export interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof statusBadgeVariants> {
  status: "live" | "development" | "offline";
}

const StatusBadge = ({ className, status, ...props }: StatusBadgeProps) => {
  return (
    <div className={cn(statusBadgeVariants({ status }), className)} {...props}>
      <div className={cn("w-2 h-2 rounded-full mr-1.5", {
        "bg-status-live": status === "live",
        "bg-status-development": status === "development", 
        "bg-status-offline": status === "offline",
      })} />
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </div>
  );
};

export { StatusBadge, statusBadgeVariants };