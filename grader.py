import random

def grade_episode(history):
    if not history:
        return {"final_score": 0.5, "total_steps": 0}
    correct = sum(1 for s in history if s.get("correct", False))
    raw = correct / len(history)
    score = round(min(0.99, max(0.01, 0.01 + raw * 0.98)), 3)
    return {
        "final_score": score,
        "total_steps": len(history)
    }