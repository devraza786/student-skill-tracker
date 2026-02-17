"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import {
  getStudents,
  createStudent,
  deleteStudent,
  updateStudent,
} from "@/lib/api";

export default function StudentsPage() {
  const { user } = useAuth();
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [editStudent, setEditStudent] = useState(null);
  const [toast, setToast] = useState(null);
  const [form, setForm] = useState({ name: "", email: "", age: "" });

  async function load() {
    try {
      const data = await getStudents();
      setStudents(data);
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  function showToast(msg, type = "success") {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  }

  function openCreate() {
    setEditStudent(null);
    setForm({ name: "", email: "", age: "" });
    setShowModal(true);
  }

  function openEdit(s) {
    setEditStudent(s);
    setForm({ name: s.name, email: s.email, age: String(s.age) });
    setShowModal(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const payload = { name: form.name, email: form.email, age: parseInt(form.age) };

    try {
      if (editStudent) {
        await updateStudent(editStudent.id, payload);
        showToast("Student updated!");
      } else {
        await createStudent(payload);
        showToast("Student created!");
      }
      setShowModal(false);
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this student?")) return;
    try {
      await deleteStudent(id);
      showToast("Student deleted!");
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  const filteredStudents = students.filter(s => 
    s.name.toLowerCase().includes(search.toLowerCase()) || 
    s.email.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <div className="loading"><div className="spinner" /></div>;

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Students</h1>
        <p className="page-subtitle">Manage your bootcamp students</p>
      </div>

      <div className="section-header">
        <div style={{ display: "flex", gap: "12px", alignItems: "center", flex: "1", maxWidth: "400px" }}>
          <div style={{ position: "relative", width: "100%" }}>
            <input 
              className="form-input" 
              placeholder="Search by name or email..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: "36px" }}
            />
            <span style={{ position: "absolute", left: "12px", top: "50%", transform: "translateY(-50%)", opacity: 0.5 }}>🔍</span>
          </div>
        </div>
        {user?.role === "teacher" && (
          <button className="btn btn-primary" onClick={openCreate}>
            + Add Student
          </button>
        )}
      </div>

      {filteredStudents.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">{search ? "🔎" : "🎓"}</div>
          <div className="empty-state-text">{search ? `No student matches "${search}"` : "No students yet"}</div>
          {user?.role === "teacher" && !search && <button className="btn btn-primary" onClick={openCreate}>Add your first student</button>}
          {search && <button className="btn btn-secondary" onClick={() => setSearch("")}>Clear search</button>}
        </div>
      ) : (
        <div className="data-grid">
          {filteredStudents.map((s) => (
            <div key={s.id} className="data-card">
              <div className="data-card-header">
                <div className="data-card-name">{s.name}</div>
                <div className="data-card-id">#{s.id}</div>
              </div>
              <div className="data-card-info">
                <span>📧 {s.email}</span>
                <span>🎂 Age: {s.age}</span>
                <span>⚡ {s.skills?.length || 0} Skills</span>
              </div>
              {s.skills && s.skills.length > 0 && (
                <div className="skill-tags">
                  {s.skills.map((sk) => (
                    <span key={sk.skill_id} className={`badge ${sk.category.toLowerCase()}`}>
                      {sk.skill_name}
                    </span>
                  ))}
                </div>
              )}
              <div className="data-card-actions">
                <Link href={`/students/${s.id}`} className="btn btn-secondary btn-sm">
                  View Details
                </Link>
                {user?.role === "teacher" && (
                  <>
                    <button className="btn btn-secondary btn-sm" onClick={() => openEdit(s)}>
                      ✏️ Edit
                    </button>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(s.id)}>
                      🗑️
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2 className="modal-title">{editStudent ? "Edit Student" : "Add Student"}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input
                  className="form-input"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  required
                  placeholder="e.g. John Doe"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Email</label>
                <input
                  className="form-input"
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  required
                  placeholder="john@example.com"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Age</label>
                <input
                  className="form-input"
                  type="number"
                  value={form.age}
                  onChange={(e) => setForm({ ...form, age: e.target.value })}
                  required
                  min="16"
                  placeholder="Must be > 15"
                />
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editStudent ? "Update" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </>
  );
}
