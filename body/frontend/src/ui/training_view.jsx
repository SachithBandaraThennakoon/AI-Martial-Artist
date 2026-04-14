import { useEffect, useState } from "react";

import SkeletonView from "../components/visualization/skeleton_view";
import MetricsPanel from "../components/feedback/metrics_panel";

export default function TrainingView() {
  const [techniques, setTechniques] = useState([]);
  const [selectedTechnique, setSelectedTechnique] = useState(null);

  const [steps, setSteps] = useState([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  const [requiredParts, setRequiredParts] = useState([]);

  const [angles, setAngles] = useState({});
  const [accuracy, setAccuracy] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [summary, setSummary] = useState("");

  // ✅ FIX: ADD THIS
  const [displayedSummary, setDisplayedSummary] = useState("🔥 Start Training");

  // -----------------------------
  // Load techniques
  // -----------------------------
  useEffect(() => {
    fetch("http://127.0.0.1:8000/techniques")
      .then(res => res.json())
      .then(data => {
        setTechniques(data);
        if (data.length > 0) {
          setSelectedTechnique(data[0].id);
        }
      });
  }, []);

  // -----------------------------
  // Load steps
  // -----------------------------
  useEffect(() => {
    if (!selectedTechnique) return;

    fetch(`http://127.0.0.1:8000/techniques/${selectedTechnique}/steps`)
      .then(res => res.json())
      .then(data => {
        setSteps(data);
        setCurrentStepIndex(0);
      });
  }, [selectedTechnique]);

  // -----------------------------
  // Load required angles
  // -----------------------------
  useEffect(() => {
    if (!steps[currentStepIndex]) return;

    fetch(
      `http://127.0.0.1:8000/steps/${steps[currentStepIndex].id}/angles`
    )
      .then(res => res.json())
      .then(data => {
        setRequiredParts(data);
      });
  }, [currentStepIndex, steps]);

  // ✅ FIX: CONTROL FEEDBACK SPEED
  useEffect(() => {
    if (summary && summary !== "...") {
      setDisplayedSummary(summary);
    }
  }, [summary]);

  return (
    <div style={styles.container}>

      {/* 🧠 SKELETON */}
      <div style={styles.skeletonWrapper}>
        <SkeletonView
          currentStepId={steps[currentStepIndex]?.id}
          requiredParts={requiredParts}
          onAngleUpdate={setAngles}
          onAccuracyUpdate={setAccuracy}
          onFeedbackUpdate={setFeedback}
          onSummaryUpdate={setSummary}
        />
      </div>

      {/* 🔥 SUMMARY BAR */}
      <div className="feedback-bar">
        <span className="feedback-text">
          {displayedSummary}
        </span>
      </div>

      {/* LEFT PANEL */}
      <div style={styles.feedbackOverlay}>
        <div style={styles.section}>
          <h1 style={styles.sectionTitle}>
            Technique: {techniques.find(t => t.id === selectedTechnique)?.name || "Select"}
          </h1>

          <h2 style={styles.sectionTitle2}>
            Step: {steps[currentStepIndex]?.step_name || "—"}
          </h2>

          {steps.map((step, index) => (
            <div
              key={step.id}
              onClick={() => setCurrentStepIndex(index)}
              style={{
                ...styles.stepItem,
                ...(index === currentStepIndex && styles.stepActive)
              }}
            >
              {step.step_name}
            </div>
          ))}
        </div>

        <h3 style={styles.feedbackTitle}>🧠 AI Coach</h3>
      </div>

      {/* RIGHT PANEL */}
      <div style={styles.metricsOverlay}>
        <MetricsPanel
          steps={steps}
          currentStepIndex={currentStepIndex}
          setCurrentStepIndex={setCurrentStepIndex}
          accuracy={accuracy}
          angles={angles}
          requiredParts={requiredParts}
          feedback={feedback}
        />
      </div>

      {/* TECHNIQUE SELECT */}
      <div style={styles.techniqueBar}>
        <select
          onChange={(e) => setSelectedTechnique(Number(e.target.value))}
        >
          <option value="">-- Select Technique --</option>
          {techniques.map(t => (
            <option key={t.id} value={t.id}>
              {t.name}
            </option>
          ))}
        </select>
      </div>

    </div>
  );
}
/* =========================
   🎨 STYLES
========================= */
const styles = {
  container: {
    height: "100vh",
    width: "100%",
    position: "relative",
    overflow: "hidden",
    background: "#000",
    fontFamily: "Segoe UI"
  },

  skeletonWrapper: {
    position: "absolute",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    zIndex: 1
  },

  feedbackOverlay: {
    position: "absolute",
    left: "40px",
    top: "30%",
    transform: "translateY(-20%)",
    zIndex: 3,
    width: "420px",
    color: "#00ff88"
  },

  section: {
    marginBottom: "25px",
    padding: "15px"
  },

  sectionTitle: {
    marginBottom: "10px",
    color: "#07f5e1",
    fontSize: "30px"
  },

  sectionTitle2: {
    marginBottom: "10px",
    color: "#07edf5",
    fontSize: "22px"
  },

  stepItem: {
    padding: "15px",
    margin: "10px 10px",
    borderRadius: "5px",
    background: "rgba(255,255,255,0.05)",
    color: "#ccc",
    width: "300px",
    cursor: "pointer"
  },

  stepActive: {
    background: "#00ff88",
    color: "#000",
    fontWeight: "bold"
  },

  feedbackTitle: {
    marginTop: "20px",
    fontSize: "22px",
    color: "#00ff88"
  },

  metricsOverlay: {
    position: "absolute",
    right: "20px",
    top: "50%",
    transform: "translateY(-50%)",
    width: "360px",
    zIndex: 3
  },

  techniqueBar: {
    position: "absolute",
    top: "55px",
    left: "65px",
    width: "400px",
    zIndex: 4
  }
};