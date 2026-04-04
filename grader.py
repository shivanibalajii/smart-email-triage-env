def grade_episode(history):
    score = 0

    for step in history:
        if step["correct"]:
            score += 1
        else:
            score -= 1

    return {
        "final_score": score,
        "total_steps": len(history)
    }