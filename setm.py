from itertools import combinations
from collections import defaultdict


def generate_candidates(prev_frequent_itemsets, k):
    """
    Generate candidate itemsets Ck from L(k-1)
    Optimized: avoid repeated sorting
    """
    candidates = set()
    prev_list = list(prev_frequent_itemsets)

    prev_list_sorted = [tuple(sorted(itemset)) for itemset in prev_list]

    for i in range(len(prev_list_sorted)):
        for j in range(i + 1, len(prev_list_sorted)):
            L1 = prev_list_sorted[i]
            L2 = prev_list_sorted[j]

            # join step: first k-2 items must match
            if L1[: k - 2] == L2[: k - 2]:
                new_candidate = frozenset(L1) | frozenset(L2)
                candidates.add(new_candidate)

    return candidates


def SETM(transactions, min_support):
    """
    Optimized SETM Algorithm with TID-lists intersection
    """
    # Convert transactions to sets for faster subset checks
    transactions = [set(txn) for txn in transactions]

    # Step 1: Build C1 with TID-lists
    C1 = defaultdict(set)
    for tid, txn in enumerate(transactions):
        for item in txn:
            C1[frozenset([item])].add(tid)

    # Step 2: Filter L1
    L = []
    L1 = {i for i, tids in C1.items() if len(tids) >= min_support}
    L.append(L1)

    # Support counts
    support_data = {itemset: len(C1[itemset]) for itemset in L1}

    k = 2
    prev_Lk = L1

    # Step 3: Iterative generation
    while prev_Lk:
        # Generate candidates
        Ck = generate_candidates(prev_Lk, k)
        if not Ck:
            break

        # Build TID-lists for Ck via intersection of subsets' TID-lists
        prev_tid_dict = {
            itemset: C1[itemset] if k == 2 else prev_Lk_tid[itemset]
            for itemset in prev_Lk
        }
        Ck_tid = defaultdict(set)

        for cand in Ck:
            subsets = [frozenset(s) for s in combinations(cand, k - 1)]
            try:
                # intersection of all subsets TID-lists
                intersect_tids = set.intersection(*(prev_tid_dict[s] for s in subsets))
            except KeyError:
                continue

            if len(intersect_tids) >= min_support:
                Ck_tid[cand] = intersect_tids

        # Filter frequent itemsets
        Lk = set(Ck_tid.keys())
        if not Lk:
            break

        L.append(Lk)
        for cand in Lk:
            support_data[cand] = len(Ck_tid[cand])

        # Prepare for next iteration
        prev_Lk = Lk
        prev_Lk_tid = Ck_tid
        k += 1

    return L, support_data
