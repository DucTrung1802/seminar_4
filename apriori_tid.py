from collections import defaultdict
from itertools import combinations


def create_C1(transactions):
    """Create candidate 1-itemsets (C1) with TID-lists."""
    C1 = defaultdict(set)
    for tid, txn in enumerate(transactions):
        for item in txn:
            C1[(item,)].add(tid)  # use tuple instead of frozenset
    return C1


def generate_candidates(prev_freq_itemsets, k):
    """
    Generate Ck from L(k−1) more efficiently.
    """
    prev_list = sorted(prev_freq_itemsets)  # already tuples, so cheap
    candidates = set()

    n = len(prev_list)
    for i in range(n):
        p = prev_list[i]
        for j in range(i + 1, n):
            q = prev_list[j]

            # join step on first k−2 elements
            if p[:-1] == q[:-1]:
                # candidate is a tuple, sorted automatically
                cand = p + (q[-1],)
                candidates.add(cand)
            else:
                break  # because list is sorted, no further matches possible

    return candidates


def apriori_tid(transactions, min_support):
    """
    Optimized Apriori-TID.
    """
    # Convert transactions to sets once
    transactions = [set(t) for t in transactions]

    # Step 1: C1
    C1 = create_C1(transactions)
    L1 = {itemset: tids for itemset, tids in C1.items() if len(tids) >= min_support}

    support_data = {itemset: len(tids) for itemset, tids in L1.items()}
    L = [list(L1.keys())]

    prev_L = L1
    k = 2

    while prev_L:
        # Generate Ck
        Ck = generate_candidates(prev_L.keys(), k)
        if not Ck:
            break

        Ck_tid = {}
        # Now candidate itemsets are tuples, create subsets efficiently
        for cand in Ck:
            # get k−1 subsets using tuple slicing instead of combinations
            subsets = (
                (
                    cand[1:],  # remove first
                    cand[:-1],  # remove last
                )
                if k == 2
                else [cand[:i] + cand[i + 1 :] for i in range(k)]
            )

            try:
                tid_lists = [prev_L[s] for s in subsets]
            except KeyError:
                continue

            # intersect tid lists (smallest first = faster)
            tid_lists.sort(key=len)
            common = tid_lists[0].intersection(*tid_lists[1:])

            if len(common) >= min_support:
                Ck_tid[cand] = common
                support_data[cand] = len(common)

        if not Ck_tid:
            break

        L.append(list(Ck_tid.keys()))
        prev_L = Ck_tid
        k += 1

    return L, support_data
