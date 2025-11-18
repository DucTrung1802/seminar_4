from collections import defaultdict
from itertools import combinations


def create_C1(transactions):
    """Create candidate 1-itemsets (C1)."""
    C1 = defaultdict(set)
    for tid, txn in enumerate(transactions):
        for item in txn:
            C1[frozenset([item])].add(tid)
    return C1


def generate_candidates(prev_freq_itemsets, k):
    """
    Generate Ck from L(k-1) using the Apriori join step.
    prev_freq_itemsets: list of frozensets
    """
    candidates = []
    Lk_1 = list(prev_freq_itemsets)
    length = len(Lk_1)

    for i in range(length):
        for j in range(i + 1, length):
            L1 = sorted(Lk_1[i])
            L2 = sorted(Lk_1[j])

            # join if first k-2 items are same
            if L1[: k - 2] == L2[: k - 2]:
                candidate = frozenset(sorted(set(L1) | set(L2)))
                candidates.append(candidate)

    return candidates


def apriori_tid(transactions, min_support):
    """
    Apriori-TID algorithm.
    Returns:
        L: list of all frequent itemsets per k
        support_data: dict { itemset : support }
    """

    # -----------------------------------------
    # STEP 1: Build 1-itemset TID lists (C1)
    # -----------------------------------------
    C1 = create_C1(transactions)

    # Filter by min-support
    L1 = {itemset: tids for itemset, tids in C1.items() if len(tids) >= min_support}

    support_data = {itemset: len(tids) for itemset, tids in L1.items()}
    L = [list(L1.keys())]  # L[0] = frequent 1-itemsets

    # APRIORI-TID database: each entry is (tid, {frequent itemsets that appear})
    # For k = 1 → the TID-list is already extracted, so database is not needed yet.

    k = 2
    prev_L = L1

    # -----------------------------------------
    # MAIN LOOP: Build Lk from L(k-1)
    # -----------------------------------------
    while prev_L:

        # Generate Ck
        Ck = generate_candidates(prev_L.keys(), k)

        # Build TID-lists for Ck using Apriori-TID method
        Ck_tidsets = defaultdict(set)

        for candidate in Ck:
            # Prepare to intersect TID lists of subsets
            subsets = [frozenset(s) for s in combinations(candidate, k - 1)]

            # Get TID-lists of all (k-1)-subsets
            try:
                tidsets = [prev_L[s] for s in subsets]
            except KeyError:
                continue  # candidate cannot be frequent

            # Intersection gives support
            common_tids = set.intersection(*tidsets)

            if len(common_tids) >= min_support:
                Ck_tidsets[candidate] = common_tids

        if not Ck_tidsets:
            break

        # Add to results
        L.append(list(Ck_tidsets.keys()))

        for itemset, tids in Ck_tidsets.items():
            support_data[itemset] = len(tids)

        # Prepare for next iteration
        prev_L = Ck_tidsets
        k += 1

    return L, support_data
