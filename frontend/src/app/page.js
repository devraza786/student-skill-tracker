"use client";

import { useEffect, useState } from "react";
import {
  getStudents,
  getSkills,
  getTopStudents,
  getMostPopularSkill,
  getJobReadyStudents,
} from "@/lib/api";

export default function DashboardPage() {
  const [students, setStudents] = useState([]);
  const [skills, setSkills] = useState([]);
  const [topStudents, setTopStudents] = useState([]);
  const [popularSkill, setPopularSkill] = useState(null);
  const [jobReady, setJobReady] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, sk, ts, ps, jr] = await Promise.all([
          getStudents(),
          getSkills(),
          getTopStudents(),
          getMostPopularSkill(),
          getJobReadyStudents(),
        ]);
        setStudents(s);
        setSkills(sk);
        setTopStudents(ts);
        setPopularSkill(ps);
        setJobReady(jr);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Overview of your bootcamp analytics</p>
      </div>

      {/* Stats Row */}
      <div className="stats-grid">
        <div className="stat-card purple">
          <div className="stat-icon purple">🎓</div>
          <div className="stat-value">{students.length}</div>
          <div className="stat-label">Total Students</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-icon teal">⚡</div>
          <div className="stat-value">{skills.length}</div>
          <div className="stat-label">Total Skills</div>
        </div>
        <div className="stat-card pink">
          <div className="stat-icon pink">🏆</div>
          <div className="stat-value">{popularSkill?.name || "—"}</div>
          <div className="stat-label">Most Popular Skill ({popularSkill?.student_count || 0} students)</div>
        </div>
        <div className="stat-card gold">
          <div className="stat-icon gold">✅</div>
          <div className="stat-value">{jobReady.length}</div>
          <div className="stat-label">Job Ready Students</div>
        </div>
      </div>

      {/* Top Students */}
      <div className="section">
        <div className="section-header">
          <h2 className="section-title">🏅 Top Students by Assessment</h2>
        </div>
        {topStudents.length > 0 ? (
          <div className="podium">
            {topStudents.length > 1 && (
              <div className="podium-item">
                <div className="podium-rank silver">2</div>
                <div className="podium-bar second">
                  <div className="podium-score">{topStudents[1].average_score}</div>
                  <div className="podium-name">{topStudents[1].name}</div>
                </div>
              </div>
            )}
            {topStudents.length > 0 && (
              <div className="podium-item">
                <div className="podium-rank gold">1</div>
                <div className="podium-bar first">
                  <div className="podium-score">{topStudents[0].average_score}</div>
                  <div className="podium-name">{topStudents[0].name}</div>
                </div>
              </div>
            )}
            {topStudents.length > 2 && (
              <div className="podium-item">
                <div className="podium-rank bronze">3</div>
                <div className="podium-bar third">
                  <div className="podium-score">{topStudents[2].average_score}</div>
                  <div className="podium-name">{topStudents[2].name}</div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">📈</div>
            <div className="empty-state-text">
              Assign skills to students to see rankings
            </div>
          </div>
        )}
      </div>

      {/* Job Ready Students */}
      <div className="section">
        <div className="section-header">
          <h2 className="section-title">✅ Job Ready Students</h2>
        </div>
        {jobReady.length > 0 ? (
          <div className="data-grid">
            {jobReady.map((s) => (
              <div key={s.student_id} className="data-card">
                <div className="data-card-header">
                  <div className="data-card-name">{s.name}</div>
                  <div className="job-ready-tag">🚀 JOB READY</div>
                </div>
                <div className="data-card-info">
                  <span>📧 {s.email}</span>
                  <span>⚡ {s.skill_count} Skills</span>
                  <span>📊 Avg Score: {s.average_score}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">🎯</div>
            <div className="empty-state-text">
              No job-ready students yet (requires 3+ skills and avg score &gt; 75)
            </div>
          </div>
        )}
      </div>
    </>
  );
}
