def calculate_risk(transaction):
    score = 0

    if transaction.amount > 10000:
        score += 70
    elif transaction.amount > 5000:
        score += 40

    if transaction.location not in ["home_city"]:
        score += 20

    return min(score, 100)
