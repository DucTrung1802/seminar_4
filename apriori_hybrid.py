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
    candidates = []
    Lk_1 = list(prev_freq_itemsets)
    n = len(Lk_1)

    for i in range(n):
        for j in range(i + 1, n):
            L1 = sorted(Lk_1[i])
            L2 = sorted(Lk_1[j])

            # join step
            if L1[: k - 2] == L2[: k - 2]:
                cand = frozenset(sorted(set(L1) | set(L2)))
                candidates.append(cand)

    return candidates


# ====================================================
#                 APRIORI-HYBRID
# ====================================================
def apriori_hybrid(transactions, min_support, threshold_ratio=0.70):
    """
    Apriori-Hybrid algorithm:
      - Run Apriori (DB scan) until candidate(TID) table becomes small
      - Then switch to Apriori-TID

    threshold_ratio:
        When #Ck falls below threshold_ratio * #C1, switch to Apriori-TID
    """

    # ---------------------------
    # STEP 1: Generate C1
    # ---------------------------
    C1 = create_C1(transactions)

    # Frequent 1-itemsets
    L1 = {item: tids for item, tids in C1.items() if len(tids) >= min_support}

    support_data = {item: len(tids) for item, tids in L1.items()}
    L = [list(L1.keys())]

    # Track size of initial candidate set
    C1_size = len(C1)

    prev_L = L1
    k = 2
    use_tid = False  # Switch flag to Apriori-TID

    # ======================================================
    #                   MAIN LOOP
    # ======================================================
    while prev_L:

        # --------------------------------------------------
        # GENERATE Ck
        # --------------------------------------------------
        Ck = generate_candidates(prev_L.keys(), k)

        if not Ck:
            break

        # Check candidate size to decide switching
        if (len(Ck) < threshold_ratio * C1_size) and not use_tid:
            use_tid = True
            # print(f"Switching to Apriori-TID at k={k}")

        # --------------------------------------------------
        # APRIORI DATABASE-SCAN MODE
        # --------------------------------------------------
        if not use_tid:

            Ck_count = defaultdict(int)

            for tid, txn in enumerate(transactions):
                txn_set = set(txn)
                for cand in Ck:
                    if cand.issubset(txn_set):
                        Ck_count[cand] += 1

            Ck_freq = {
                c: count for c, count in Ck_count.items() if count >= min_support
            }

            if not Ck_freq:
                break

            L.append(list(Ck_freq.keys()))

            for itemset, count in Ck_freq.items():
                support_data[itemset] = count

            # Prepare TID-lists for next iteration if hybrid may switch
            prev_L = {c: set() for c in Ck_freq.keys()}

            # Build TID-lists only once here
            for tid, txn in enumerate(transactions):
                txn_set = set(txn)
                for c in prev_L.keys():
                    if c.issubset(txn_set):
                        prev_L[c].add(tid)

        # --------------------------------------------------
        # APRIORI-TID MODE
        # --------------------------------------------------
        else:
            Ck_tid = defaultdict(set)

            for cand in Ck:
                subsets = [frozenset(s) for s in combinations(cand, k - 1)]

                try:
                    tidsets = [prev_L[s] for s in subsets]
                except KeyError:
                    continue

                intersect_tids = set.intersection(*tidsets)

                if len(intersect_tids) >= min_support:
                    Ck_tid[cand] = intersect_tids

            if not Ck_tid:
                break

            L.append(list(Ck_tid.keys()))

            for itemset, tids in Ck_tid.items():
                support_data[itemset] = len(tids)

            prev_L = Ck_tid

        k += 1

    return L, support_data
