"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  getStudent,
  getSkills,
  assignSkill,
  getAverageProficiency,
} from "@/lib/api";

export default function StudentDetailPage() {
  const params = useParams();
  const studentId = params.id;

  const [student, setStudent] = useState(null);
  const [allSkills, setAllSkills] = useState([]);
  const [avgProf, setAvgProf] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAssign, setShowAssign] = useState(false);
  const [toast, setToast] = useState(null);
  const [form, setForm] = useState({
    skill_id: "",
    proficiency_level: "3",
    assessment_score: "70",
  });

  async function load() {
    try {
      const [s, sk, ap] = await Promise.all([
        getStudent(studentId),
        getSkills(),
        getAverageProficiency(studentId),
      ]);
      setStudent(s);
      setAllSkills(sk);
      setAvgProf(ap);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, [studentId]);

  function showToast(msg, type = "success") {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  }

  async function handleAssign(e) {
    e.preventDefault();
    try {
      await assignSkill(studentId, {
        skill_id: parseInt(form.skill_id),
        proficiency_level: parseInt(form.proficiency_level),
        assessment_score: parseInt(form.assessment_score),
      });
      showToast("Skill assigned!");
      setShowAssign(false);
      setForm({ skill_id: "", proficiency_level: "3", assessment_score: "70" });
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  if (loading) return <div className="loading"><div className="spinner" /></div>;
  if (!student) return <div className="empty-state"><div className="empty-state-text">Student not found</div></div>;

  return (
    <>
      <Link href="/students" className="back-link">← Back to Students</Link>

      <div className="detail-header">
        <div className="detail-avatar">{student.name.charAt(0)}</div>
        <div>
          <h1 className="page-title">{student.name}</h1>
          <p className="page-subtitle">{student.email} · Age {student.age}</p>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card purple">
          <div className="stat-icon purple">⚡</div>
          <div className="stat-value">{student.skills?.length || 0}</div>
          <div className="stat-label">Skills Assigned</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-icon teal">📊</div>
          <div className="stat-value">{avgProf?.average_proficiency ?? "—"}</div>
          <div className="stat-label">Avg Proficiency</div>
        </div>
        <div className="stat-card gold">
          <div className="stat-icon gold">📈</div>
          <div className="stat-value">
            {student.skills?.length > 0
              ? (student.skills.reduce((a, s) => a + s.assessment_score, 0) / student.skills.length).toFixed(1)
              : "—"}
          </div>
          <div className="stat-label">Avg Assessment Score</div>
        </div>
      </div>

      {/* Skills Section */}
      <div className="section">
        <div className="section-header">
          <h2 className="section-title">Assigned Skills</h2>
          <button className="btn btn-primary" onClick={() => setShowAssign(true)}>
            + Assign Skill
          </button>
        </div>

        {student.skills && student.skills.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Category</th>
                  <th>Proficiency</th>
                  <th>Assessment Score</th>
                </tr>
              </thead>
              <tbody>
                {student.skills.map((sk) => (
                  <tr key={sk.skill_id}>
                    <td style={{ fontWeight: 600 }}>{sk.skill_name}</td>
                    <td>
                      <span className={`badge ${sk.category.toLowerCase()}`}>{sk.category}</span>
                    </td>
                    <td>
                      <div className="proficiency-bar">
                        {[1, 2, 3, 4, 5].map((n) => (
                          <div
                            key={n}
                            className={`proficiency-dot ${n <= sk.proficiency_level ? "filled" : ""}`}
                          />
                        ))}
                      </div>
                    </td>
                    <td>
                      <div className="score-bar-wrapper">
                        <div className="score-bar">
                          <div
                            className={`score-bar-fill ${sk.assessment_score >= 75 ? "high" : sk.assessment_score >= 50 ? "mid" : "low"}`}
                            style={{ width: `${sk.assessment_score}%` }}
                          />
                        </div>
                        <span className="score-value">{sk.assessment_score}</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">⚡</div>
            <div className="empty-state-text">No skills assigned yet</div>
            <button className="btn btn-primary" onClick={() => setShowAssign(true)}>
              Assign first skill
            </button>
          </div>
        )}
      </div>

      {/* Assign Modal */}
      {showAssign && (
        <div className="modal-overlay" onClick={() => setShowAssign(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2 className="modal-title">Assign Skill to {student.name}</h2>
            <form onSubmit={handleAssign}>
              <div className="form-group">
                <label className="form-label">Skill</label>
                <select
                  className="form-select"
                  value={form.skill_id}
                  onChange={(e) => setForm({ ...form, skill_id: e.target.value })}
                  required
                >
                  <option value="">Select a skill</option>
                  {allSkills.map((sk) => (
                    <option key={sk.id} value={sk.id}>
                      {sk.name} ({sk.category})
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Proficiency Level (1-5)</label>
                <input
                  className="form-input"
                  type="number"
                  min="1"
                  max="5"
                  value={form.proficiency_level}
                  onChange={(e) => setForm({ ...form, proficiency_level: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Assessment Score (0-100)</label>
                <input
                  className="form-input"
                  type="number"
                  min="0"
                  max="100"
                  value={form.assessment_score}
                  onChange={(e) => setForm({ ...form, assessment_score: e.target.value })}
                  required
                />
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAssign(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">Assign</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </>
  );
}
