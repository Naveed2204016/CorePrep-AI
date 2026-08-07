import { ArrowRight } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  to?: string;
}

const FeatureCard = ({
  icon: Icon,
  title,
  description,
  to = "/signin",
}: FeatureCardProps) => {
  return (
    <div className="feature-card">
      <div className="feature-card-icon">
        <Icon size={24} />
      </div>

      <h3>{title}</h3>

      <p>{description}</p>

      <Link to={to} className="feature-link">
        Explore
        <ArrowRight size={16} />
      </Link>
    </div>
  );
};

export default FeatureCard;