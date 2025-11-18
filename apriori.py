from itertools import combinations
from collections import defaultdict


def apriori(transactions, min_support):
    """
    Faster Apriori implementation with minor optimizations
    """
    # Convert each transaction to set once
    transactions = list(map(set, transactions))

    # Count 1-itemsets
    item_counts = defaultdict(int)
    for txn in transactions:
        for item in txn:
            item_counts[frozenset([item])] += 1

    # Filter frequent 1-itemsets
    L1 = {item for item, count in item_counts.items() if count >= min_support}
    support_data = {
        item: count for item, count in item_counts.items() if count >= min_support
    }

    L = [L1]
    k = 2

    while True:
        prev_Lk = L[-1]
        if not prev_Lk:
            break

        # Generate candidates
        candidates = generate_candidates(prev_Lk, k)

        # Count support efficiently
        candidate_counts = defaultdict(int)
        for txn in transactions:
            # Only check candidates whose items are subset of txn
            for cand in candidates:
                if cand.issubset(txn):
                    candidate_counts[cand] += 1

        # Filter by min_support
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
    Generate Ck from L(k−1) efficiently.
    """
    candidates = set()
    prev_Lk_list = list(prev_Lk)

    for i in range(len(prev_Lk_list)):
        for j in range(i + 1, len(prev_Lk_list)):
            a = prev_Lk_list[i]
            b = prev_Lk_list[j]

            # Join step only if first k-2 items are equal
            a_list = sorted(a)
            b_list = sorted(b)
            if a_list[: k - 2] == b_list[: k - 2]:
                candidates.add(frozenset(a | b))

    return candidates
