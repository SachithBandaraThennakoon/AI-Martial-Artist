def generate_feedback(analysis):
    feedback = []

    for item in analysis:
        if item["issue"] == "too_low":
            feedback.append(f"Increase {item['body_part']}")
        elif item["issue"] == "too_high":
            feedback.append(f"Decrease {item['body_part']}")

    if not feedback:
        return "Perfect form!"

    return ". ".join(feedback)