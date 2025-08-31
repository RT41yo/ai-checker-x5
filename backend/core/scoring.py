def clamp(v, lo=0, hi=3):
    return max(lo, min(hi, v))

def compute_total(scores: dict, weights: dict) -> float:
    """
    scores: {"hard":{"correctness":int, "completeness":int}, "soft":{"clarity":int,"structure":int}}
    weights: {"hard.correctness":w,...}
    """
    total = 0.0
    acc_w = 0.0
    for path, w in weights.items():
        part = scores
        for key in path.split("."):
            part = part[key]
        total += clamp(part) * w
        acc_w += w
    if acc_w == 0:
        return 0.0
    return round(total / acc_w, 2)
