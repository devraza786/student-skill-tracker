"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth";
import { loginUser, registerUser } from "@/lib/api";

export default function LoginPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");
  const { login } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      if (isLogin) {
        const res = await loginUser({ email, password });
        login(res.user, res.access_token);
      } else {
        await registerUser({ email, password, role });
        setIsLogin(true);
        alert("Registered! Please login.");
      }
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-tabs">
          <button 
            className={`auth-tab ${isLogin ? "active" : ""}`} 
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button 
            className={`auth-tab ${!isLogin ? "active" : ""}`} 
            onClick={() => setIsLogin(false)}
          >
            SignUp
          </button>
        </div>

        <h1 className="auth-title">{isLogin ? "Welcome Back" : "Create Account"}</h1>
        <p className="auth-subtitle">
          {isLogin ? "Login to your SkillTrack account" : "Join the skill tracking platform"}
        </p>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="name@example.com"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label className="form-label">I am a...</label>
              <select 
                className="form-select" 
                value={role} 
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
              </select>
            </div>
          )}

          {error && <div className="auth-error">{error}</div>}

          <button type="submit" className="btn btn-primary auth-btn">
            {isLogin ? "Login" : "Sign Up"}
          </button>
        </form>
      </div>

      <style jsx>{`
        .auth-container {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 80vh;
        }
        .auth-card {
          background: var(--bg-secondary);
          padding: 40px;
          border-radius: 24px;
          width: 100%;
          max-width: 400px;
          box-shadow: var(--shadow-lg);
          border: 1px solid var(--border);
        }
        .auth-tabs {
          display: flex;
          background: var(--bg-primary);
          padding: 4px;
          border-radius: 12px;
          margin-bottom: 32px;
        }
        .auth-tab {
          flex: 1;
          padding: 10px;
          border-radius: 10px;
          border: none;
          background: none;
          color: var(--text-secondary);
          font-weight: 600;
          cursor: pointer;
          transition: var(--transition);
        }
        .auth-tab.active {
          background: var(--bg-card);
          color: var(--text-primary);
          box-shadow: var(--shadow-sm);
        }
        .auth-title {
          font-size: 1.75rem;
          margin-bottom: 8px;
          text-align: center;
          font-weight: 800;
        }
        .auth-subtitle {
          color: var(--text-secondary);
          text-align: center;
          margin-bottom: 32px;
          font-size: 0.9rem;
        }
        .auth-form {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        .auth-btn {
          width: 100%;
          padding: 14px;
          font-size: 1rem;
          margin-top: 10px;
        }
        .auth-error {
          color: #ff6b6b;
          background: rgba(255, 107, 107, 0.1);
          padding: 12px;
          border-radius: 8px;
          font-size: 0.85rem;
          text-align: center;
          border: 1px solid rgba(255, 107, 107, 0.2);
        }
      `}</style>
    </div>
  );
}
 Riverside
