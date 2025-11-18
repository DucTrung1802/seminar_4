from collections import defaultdict
from itertools import combinations


def create_C1(transactions):
    """Create candidate 1-itemsets (C1) with TID-lists."""
    C1 = defaultdict(set)
    for tid, txn in enumerate(transactions):
        for item in txn:
            C1[frozenset([item])].add(tid)
    return C1


def generate_candidates(prev_freq_itemsets, k):
    """
    Generate Ck from L(k-1) efficiently:
    - Avoid repeated sorting
    - Work with tuples for join
    """
    candidates = set()
    prev_list = list(prev_freq_itemsets)
    prev_list_sorted = [tuple(sorted(itemset)) for itemset in prev_list]

    for i in range(len(prev_list_sorted)):
        for j in range(i + 1, len(prev_list_sorted)):
            L1, L2 = prev_list_sorted[i], prev_list_sorted[j]

            if L1[: k - 2] == L2[: k - 2]:  # join step
                candidates.add(frozenset(L1) | frozenset(L2))

    return candidates


def apriori_tid(transactions, min_support):
    """
    Optimized Apriori-TID algorithm.
    Returns:
        L: list of frequent itemsets per size
        support_data: dict {itemset: support}
    """
    # Convert transactions to sets once (optional, improves issubset speed)
    transactions = [set(txn) for txn in transactions]

    # Step 1: C1
    C1 = create_C1(transactions)
    L1 = {itemset: tids for itemset, tids in C1.items() if len(tids) >= min_support}
    support_data = {itemset: len(tids) for itemset, tids in L1.items()}
    L = [list(L1.keys())]

    k = 2
    prev_L = L1

    while prev_L:
        # Generate Ck
        Ck = generate_candidates(prev_L.keys(), k)
        if not Ck:
            break

        # Build TID-lists for Ck via intersection of subsets
        Ck_tid = {}
        for cand in Ck:
            # subsets of size k-1
            subsets = [frozenset(s) for s in combinations(cand, k - 1)]

            # Incremental intersection (avoid *tidsets unpacking)
            try:
                tid_iter = iter(subset_tids := [prev_L[s] for s in subsets])
            except KeyError:
                continue

            common_tids = next(tid_iter).copy()
            for tidset in tid_iter:
                common_tids &= tidset
                if len(common_tids) < min_support:
                    break  # early pruning

            if len(common_tids) >= min_support:
                Ck_tid[cand] = common_tids

        if not Ck_tid:
            break

        # Store frequent itemsets and supports
        L.append(list(Ck_tid.keys()))
        for itemset, tids in Ck_tid.items():
            support_data[itemset] = len(tids)

        prev_L = Ck_tid
        k += 1

    return L, support_data
