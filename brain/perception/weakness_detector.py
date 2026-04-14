def detect_weaknesses(angle_results):
    feedback = []
    correct_parts = 0
    total_parts = len(angle_results)

    for part in angle_results:
        body = part["body_part"]
        status = part["status"]

        if status == "correct":
            correct_parts += 1
        elif status == "low":
            feedback.append(f"Increase {body} angle")
        elif status == "high":
            feedback.append(f"Decrease {body} angle")

    if total_parts == 0:
        return {
            "accuracy": 0,
            "feedback": ["No matching body parts detected"]
        }

    accuracy = round((correct_parts / total_parts) * 100, 2)

    if not feedback:
        feedback.append("Perfect form!")

    return {
        "accuracy": accuracy,
        "feedback": feedback
    }