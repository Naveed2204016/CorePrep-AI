import { Navigate } from "react-router-dom";

interface Props {
  children: React.ReactNode;
}

const ProtectedRoute = ({ children }: Props) => {

  const token = localStorage.getItem(
    "coreprep_token"
  );

  if (!token) {
    console.log("ekhane ashche");
    return <Navigate to="/signin" replace />;
  }

  return children;
};

export default ProtectedRoute;