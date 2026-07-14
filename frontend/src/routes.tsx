import { createBrowserRouter } from "react-router-dom";

import { ErrorPage } from "./components/feedback/ErrorPage";
import { NotFoundPage } from "./components/feedback/NotFoundPage";
import { AppLayout } from "./components/layout/AppLayout";
import { AIConciergePage } from "./pages/AIConcierge";
import { AdminDashboardPage } from "./pages/AdminDashboard";
import { AppointmentsPage } from "./pages/Appointments";
import { DoctorDashboardPage } from "./pages/DoctorDashboard";
import { LandingPage } from "./pages/Landing";
import { LoginPage } from "./pages/Login";
import { PatientDashboardPage } from "./pages/PatientDashboard";
import { ReceptionDashboardPage } from "./pages/ReceptionDashboard";
import { RegisterPage } from "./pages/Register";
import { SettingsPage } from "./pages/Settings";

export const router = createBrowserRouter([
  {
    path: "/",
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <LandingPage />,
      },
      {
        path: "login",
        element: <LoginPage />,
      },
      {
        path: "register",
        element: <RegisterPage />,
      },
      {
        element: <AppLayout />,
        children: [
          { path: "patient", element: <PatientDashboardPage /> },
          { path: "reception", element: <ReceptionDashboardPage /> },
          { path: "admin", element: <AdminDashboardPage /> },
          { path: "doctor", element: <DoctorDashboardPage /> },
          { path: "ai-concierge", element: <AIConciergePage /> },
          { path: "appointments", element: <AppointmentsPage /> },
          { path: "settings", element: <SettingsPage /> },
        ],
      },
      {
        path: "*",
        element: <NotFoundPage />,
      },
    ],
  },
]);
