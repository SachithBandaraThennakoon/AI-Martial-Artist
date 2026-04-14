import { useContext } from "react";
import { AuthContext } from "../../memory/working_memory/auth_context";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const { token } = useContext(AuthContext);

  if (!token) {
    return <Navigate to="/login" />;
  }

  return children;
}