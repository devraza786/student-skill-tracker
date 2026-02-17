"use client";

import "./globals.css";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { AuthProvider, useAuth } from "@/lib/auth";
import ProtectedRoute from "@/components/ProtectedRoute";

const navItems = [
  { href: "/", label: "Dashboard", icon: "📊" },
  { href: "/students", label: "Students", icon: "🎓" },
  { href: "/skills", label: "Skills", icon: "⚡" },
];

export default function RootLayout({ children }) {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <html lang="en">
      <head>
        <title>SkillTrack — Student Analytics</title>
        <meta name="description" content="Student Skill Tracking & Analytics Dashboard" />
      </head>
      <body>
        <AuthProvider>
          <ProtectedRoute>
            <div className="app-layout">
              <aside className="sidebar">
                <div className="sidebar-logo">
                  <div className="sidebar-logo-icon">S</div>
                  <div className="sidebar-logo-text">
                    Skill<span>Track</span>
                  </div>
                </div>
                <nav className="sidebar-nav">
                  {navItems.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`sidebar-link ${pathname === item.href ? "active" : ""}`}
                    >
                      <span className="sidebar-link-icon">{item.icon}</span>
                      {item.label}
                    </Link>
                  ))}
                </nav>

                <div className="sidebar-footer">
                  {user ? (
                    <div className="user-profile">
                      <div className="user-info">
                        <div className="user-email">{user.email}</div>
                        <div className="user-role badge">{user.role}</div>
                      </div>
                      <button className="btn btn-secondary btn-sm" style={{ width: "100%", marginTop: "12px" }} onClick={logout}>
                        🚪 Logout
                      </button>
                    </div>
                  ) : (
                    <Link href="/login" className="btn btn-primary btn-sm" style={{ width: "100%", textAlign: "center", display: "block" }}>
                      🔑 Login
                    </Link>
                  )}
                </div>
              </aside>
              <main className="main-content">
                {children}
              </main>
            </div>
          </ProtectedRoute>
        </AuthProvider>
      </body>
    </html>
  );
}
