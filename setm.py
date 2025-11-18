from itertools import combinations
from collections import defaultdict


def generate_candidates(prev_frequent_itemsets, k):
    """
    Generate candidate itemsets Ck from L(k-1)
    """
    candidates = set()
    prev_list = list(prev_frequent_itemsets)

    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            L1 = list(prev_list[i])
            L2 = list(prev_list[j])
            L1.sort()
            L2.sort()

            # join step
            if L1[: k - 2] == L2[: k - 2]:
                new_candidate = frozenset(prev_list[i] | prev_list[j])
                candidates.add(new_candidate)

    return candidates


def SETM(transactions, min_support):
    """
    SETM Algorithm:
    - C_k is maintained with TID-lists
    - L_k is derived by filtering C_k

    params:
        transactions: list of list integers
        min_support: absolute support threshold
    """

    # Build initial C1 (1-itemsets) with TID-lists
    C1 = defaultdict(set)
    for tid, txn in enumerate(transactions):
        for item in txn:
            C1[frozenset([item])].add(tid)

    # Derive L1 by filtering C1
    L = []
    L1 = {i for i, tids in C1.items() if len(tids) >= min_support}
    L.append(L1)

    # Store support counts
    support_data = {itemset: len(C1[itemset]) for itemset in L1}

    k = 2
    prev_Lk = L1

    # iterative steps for k ≥ 2
    while prev_Lk:
        # 1. Generate Ck
        Ck = generate_candidates(prev_Lk, k)

        # 2. Construct TID-lists for Ck
        Ck_tidlists = defaultdict(set)

        for cand in Ck:
            for tid, txn in enumerate(transactions):
                if cand.issubset(txn):
                    Ck_tidlists[cand].add(tid)

        # 3. Filter to produce Lk
        Lk = {
            cand for cand, tidlist in Ck_tidlists.items() if len(tidlist) >= min_support
        }

        if not Lk:
            break

        L.append(Lk)

        # update support data
        for cand in Lk:
            support_data[cand] = len(Ck_tidlists[cand])

        prev_Lk = Lk
        k += 1

    return L, support_data
