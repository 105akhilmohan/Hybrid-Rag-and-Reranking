def precision_at_k(retrieved_ids, relevant_ids, k):
    retrieved = retrieved_ids[:k]
    if not retrieved:
        return 0.0
    relevant = set(relevant_ids)
    return sum(item in relevant for item in retrieved) / len(retrieved)


def recall_at_k(retrieved_ids, relevant_ids, k):
    relevant = set(relevant_ids)
    if not relevant:
        return 0.0
    retrieved = set(retrieved_ids[:k])
    return len(retrieved.intersection(relevant)) / len(relevant)


def reciprocal_rank(retrieved_ids, relevant_ids):
    relevant = set(relevant_ids)
    for rank, item in enumerate(retrieved_ids, start=1):
        if item in relevant:
            return 1.0 / rank
    return 0.0
