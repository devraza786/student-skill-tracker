"use client";

import { useEffect, useState } from "react";
import { getSkills, createSkill, deleteSkill } from "@/lib/api";

const CATEGORIES = ["Frontend", "Backend", "DevOps", "AI"];

export default function SkillsPage() {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterCat, setFilterCat] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [toast, setToast] = useState(null);
  const [form, setForm] = useState({ name: "", category: "Backend" });

  async function load() {
    try {
      const data = await getSkills(filterCat || undefined);
      setSkills(data);
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, [filterCat]);

  function showToast(msg, type = "success") {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  }

  async function handleCreate(e) {
    e.preventDefault();
    try {
      await createSkill(form);
      showToast("Skill created!");
      setShowModal(false);
      setForm({ name: "", category: "Backend" });
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this skill?")) return;
    try {
      await deleteSkill(id);
      showToast("Skill deleted!");
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  if (loading) return <div className="loading"><div className="spinner" /></div>;

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Skills</h1>
        <p className="page-subtitle">Manage available bootcamp skills</p>
      </div>

      <div className="section-header">
        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
          <button
            className={`btn btn-sm ${filterCat === "" ? "btn-primary" : "btn-secondary"}`}
            onClick={() => setFilterCat("")}
          >
            All
          </button>
          {CATEGORIES.map((c) => (
            <button
              key={c}
              className={`btn btn-sm ${filterCat === c ? "btn-primary" : "btn-secondary"}`}
              onClick={() => setFilterCat(c)}
            >
              {c}
            </button>
          ))}
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          + Add Skill
        </button>
      </div>

      {skills.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">⚡</div>
          <div className="empty-state-text">No skills found</div>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>Add your first skill</button>
        </div>
      ) : (
        <div className="data-grid">
          {skills.map((sk) => (
            <div key={sk.id} className="data-card">
              <div className="data-card-header">
                <div className="data-card-name">{sk.name}</div>
                <span className={`badge ${sk.category.toLowerCase()}`}>{sk.category}</span>
              </div>
              <div className="data-card-actions">
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(sk.id)}>
                  🗑️ Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2 className="modal-title">Add Skill</h2>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Skill Name</label>
                <input
                  className="form-input"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  required
                  placeholder="e.g. Python, React, Docker"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Category</label>
                <select
                  className="form-select"
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value })}
                >
                  {CATEGORIES.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </>
  );
}
