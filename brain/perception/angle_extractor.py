from brain.memory.semantic_memory.target_angle import TargetAngle


def extract_angle_accuracy(db, step_id: int, live_angles: dict):
    target_angles = db.query(TargetAngle).filter(
        TargetAngle.step_id == step_id
    ).all()

    results = []

    for target in target_angles:
        body_part = target.body_part
        live_value = live_angles.get(body_part)

        if live_value is None:
            continue

        if target.min_angle <= live_value <= target.max_angle:
            status = "correct"
        elif live_value < target.min_angle:
            status = "low"
        else:
            status = "high"

        results.append({
            "body_part": body_part,
            "value": live_value,
            "target": (target.min_angle, target.max_angle),
            "status": status
        })

    return results