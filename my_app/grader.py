import random
def grade(rewards):
    if not rewards:
        return 0.5
    raw = sum(rewards) / len(rewards)
    return round(min(0.99, max(0.01, 0.01 + raw * 0.98)), 3)