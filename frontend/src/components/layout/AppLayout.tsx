import { Outlet } from "react-router-dom";

import { SidebarLayout } from "./SidebarLayout";
import { TopNavigation } from "./TopNavigation";

export function AppLayout() {
  return (
    <SidebarLayout>
      <TopNavigation />
      <main className="min-h-[calc(100vh-4rem)] px-6 py-6 lg:px-8">
        <Outlet />
      </main>
    </SidebarLayout>
  );
}
