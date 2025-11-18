from collections import defaultdict
from itertools import combinations


# ----------------------------------------------------
# Helper: Create C1 (1-item candidates)
# ----------------------------------------------------
def create_C1(transactions):
    C1 = defaultdict(set)
    for tid, txn in enumerate(transactions):
        for item in txn:
            C1[frozenset([item])].add(tid)
    return C1


# ----------------------------------------------------
# Helper: Generate Ck from L(k-1)
# ----------------------------------------------------
def generate_candidates(prev_freq_itemsets, k):
    candidates = set()
    prev_list = list(prev_freq_itemsets)
    prev_list_sorted = [tuple(sorted(itemset)) for itemset in prev_list]

    n = len(prev_list_sorted)
    for i in range(n):
        for j in range(i + 1, n):
            L1, L2 = prev_list_sorted[i], prev_list_sorted[j]
            if L1[: k - 2] == L2[: k - 2]:  # join step
                candidates.add(frozenset(L1) | frozenset(L2))
    return candidates


# ====================================================
#                 APRIORI-HYBRID (Optimized)
# ====================================================
def apriori_hybrid(transactions, min_support, threshold_ratio=0.7):
    """
    Apriori-Hybrid: database scan + TID-list switching
    """

    # Convert transactions to sets once
    transactions = [set(txn) for txn in transactions]

    # Step 1: C1
    C1 = create_C1(transactions)
    L1 = {item: tids for item, tids in C1.items() if len(tids) >= min_support}
    support_data = {item: len(tids) for item, tids in L1.items()}
    L = [list(L1.keys())]

    C1_size = len(C1)
    prev_L = L1
    k = 2
    use_tid = False

    while prev_L:
        # Generate Ck
        Ck = generate_candidates(prev_L.keys(), k)
        if not Ck:
            break

        # Decide whether to switch to TID mode
        if not use_tid and len(Ck) < threshold_ratio * C1_size:
            use_tid = True

        # -----------------------
        # DATABASE SCAN MODE
        # -----------------------
        if not use_tid:
            Ck_count = defaultdict(int)

            for txn in transactions:
                for cand in Ck:
                    if cand.issubset(txn):
                        Ck_count[cand] += 1

            # Filter by min_support
            Ck_freq = {
                c: count for c, count in Ck_count.items() if count >= min_support
            }
            if not Ck_freq:
                break

            L.append(list(Ck_freq.keys()))
            support_data.update(Ck_freq)

            # Build TID-lists for next iteration
            prev_L = {c: set() for c in Ck_freq.keys()}
            for tid, txn in enumerate(transactions):
                for c in prev_L.keys():
                    if c.issubset(txn):
                        prev_L[c].add(tid)

        # -----------------------
        # TID-LIST MODE
        # -----------------------
        else:
            Ck_tid = {}
            for cand in Ck:
                subsets = [frozenset(s) for s in combinations(cand, k - 1)]
                try:
                    tid_iter = iter([prev_L[s] for s in subsets])
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

            L.append(list(Ck_tid.keys()))
            for itemset, tids in Ck_tid.items():
                support_data[itemset] = len(tids)

            prev_L = Ck_tid

        k += 1

    return L, support_data
