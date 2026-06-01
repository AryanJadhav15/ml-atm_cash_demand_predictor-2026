import { NavLink, Outlet } from "react-router-dom";
import ThemeToggle from "../components/ThemeToggle.jsx";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/atms", label: "ATM Fleet" },
];

export default function AppLayout() {
  return (
    <div className="min-h-screen text-text">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-border bg-panel/95 p-6 lg:block">
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-accent">Cash Ops</p>
          <h1 className="mt-3 text-2xl font-semibold tracking-normal">ATM Intelligence</h1>
        </div>
        <nav className="mt-10 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `block rounded-lg px-4 py-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-accent text-white"
                    : "text-muted hover:bg-hover hover:text-text"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-20 border-b border-border bg-background/85 px-5 py-4 backdrop-blur lg:px-8">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-muted">Operations dashboard</p>
              <p className="text-lg font-semibold">ATM Cash Intelligence System</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex gap-2 lg:hidden">
                {navItems.map((item) => (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={({ isActive }) =>
                      `rounded-lg px-3 py-2 text-sm ${
                        isActive ? "bg-accent text-white" : "bg-hover text-muted"
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
              </div>
              <ThemeToggle />
            </div>
          </div>
        </header>
        <main className="px-5 py-6 lg:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
