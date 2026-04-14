import { BrowserRouter, Routes, Route } from "react-router-dom";

// 🧠 MEMORY
import { AuthProvider } from "./memory/working_memory/auth_context";

// 🧭 NAVIGATION
import Navbar from "./components/navigation/navbar";

// 🔐 PROTECTION
import ProtectedRoute from "./components/protection/protected_route";

// 🧍 UI (BODY)
import HomeView from "./ui/home_view";
import TrainingView from "./ui/training_view";

// 🤝 INTERACTION
import LoginView from "./interaction/login_view";
import RegisterView from "./interaction/register_view";


function App() {
  return (
    <AuthProvider>
      <BrowserRouter>

        <Navbar />

        <Routes>
          <Route path="/" element={<HomeView />} />

          <Route path="/login" element={<LoginView />} />
          <Route path="/register" element={<RegisterView />} />

          <Route
            path="/training"
            element={
              <ProtectedRoute>
                <TrainingView />
              </ProtectedRoute>
            }
          />
        </Routes>

      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;