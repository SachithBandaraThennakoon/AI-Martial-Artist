from brain.perception.angle_extractor import extract_angle_accuracy
from brain.perception.weakness_detector import detect_weaknesses


def run_perception(db, step_id, live_angles):
    # 1️⃣ Extract angle status
    angle_results = extract_angle_accuracy(db, step_id, live_angles)

    # 2️⃣ Detect weaknesses
    result = detect_weaknesses(angle_results)

    return result