const API_BASE = "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Something went wrong" }));
    throw new Error(err.detail || `Error ${res.status}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

// Students
export const getStudents = () => request("/students/");
export const getStudent = (id) => request(`/students/${id}`);
export const createStudent = (data) => request("/students/", { method: "POST", body: JSON.stringify(data) });
export const updateStudent = (id, data) => request(`/students/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteStudent = (id) => request(`/students/${id}`, { method: "DELETE" });
export const assignSkill = (studentId, data) => request(`/students/${studentId}/skills`, { method: "POST", body: JSON.stringify(data) });

// Skills
export const getSkills = (category) => request(`/skills/${category ? `?category=${category}` : ""}`);
export const createSkill = (data) => request("/skills/", { method: "POST", body: JSON.stringify(data) });
export const deleteSkill = (id) => request(`/skills/${id}`, { method: "DELETE" });

// Analytics
export const getAverageProficiency = (id) => request(`/analytics/students/${id}/average-proficiency`);
export const getTopStudents = () => request("/analytics/top-students");
export const getMostPopularSkill = () => request("/analytics/most-popular-skill");
export const getJobReadyStudents = () => request("/analytics/job-ready-students");
