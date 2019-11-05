import random


def choose_random(values, k=1):
    if len(values) < k:
        k = len(values)
    results = random.choices(values, k=k)
    if k == 1:
        return results[0]
    return results
