# -----------------------------------------
#   Apriori Algorithm (Simple Implementation)
# -----------------------------------------

from itertools import combinations
from collections import defaultdict


def apriori(transactions, min_support):
    """
    transactions: list of lists (each a list of item integers)
    min_support: absolute threshold (e.g., 100 means appears ≥100 times)
    """
    # Count 1-itemsets
    item_counts = defaultdict(int)
    for txn in transactions:
        for item in txn:
            item_counts[frozenset([item])] += 1

    # Filter L1
    L = [{i for i, c in item_counts.items() if c >= min_support}]
    support_data = {i: c for i, c in item_counts.items() if c >= min_support}

    k = 2
    while True:
        prev_Lk = L[-1]
        candidates = generate_candidates(prev_Lk, k)

        candidate_counts = defaultdict(int)

        for txn in transactions:
            txn_set = set(txn)
            for cand in candidates:
                if cand.issubset(txn_set):
                    candidate_counts[cand] += 1

        Lk = {cand for cand, count in candidate_counts.items() if count >= min_support}

        if not Lk:
            break

        L.append(Lk)
        support_data.update(
            {
                cand: count
                for cand, count in candidate_counts.items()
                if count >= min_support
            }
        )
        k += 1

    return L, support_data


def generate_candidates(prev_Lk, k):
    """
    Generate Ck from L(k−1)
    """
    candidates = set()
    prev_Lk_list = list(prev_Lk)

    for i in range(len(prev_Lk_list)):
        for j in range(i + 1, len(prev_Lk_list)):
            a = list(prev_Lk_list[i])
            b = list(prev_Lk_list[j])
            a.sort()
            b.sort()

            if a[: k - 2] == b[: k - 2]:
                candidates.add(frozenset(prev_Lk_list[i] | prev_Lk_list[j]))

    return candidates
