from brain.awareness.movement_analysis import analyze_movement
from brain.cognition.coaching import generate_feedback
from brain.temporal.trend_analysis import summarize_movement


def run_brain(required_parts, live_angles, history):
    # 1️⃣ Awareness
    analysis = analyze_movement(required_parts, live_angles)

    # 2️⃣ Cognition (AI coaching)
    feedback = generate_feedback(analysis)

    # 3️⃣ Temporal (trend understanding)
    summary = summarize_movement(history, live_angles, required_parts)

    return {
        "analysis": analysis,
        "feedback": feedback,
        "summary": summary
    }