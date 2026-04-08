def grade(rewards):
    if not rewards:
        return 0.5
    total = sum(rewards)
    max_score = len(rewards)
    raw = total / max_score
    return round(min(0.99, max(0.01, 0.01 + raw * 0.98)), 3)