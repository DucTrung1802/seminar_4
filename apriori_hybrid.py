from efficient_apriori import apriori


def apriori_hybrid(transactions, min_support, threshold_ratio=0.7):
    """
    Replacement for your Apriori-Hybrid implementation using efficient-apriori.

    Maintains the same return structure:

        L: [
              [frozenset(...), ...],   # L1
              [frozenset(...), ...],   # L2
              ...
           ]

        support_data: {frozenset(...): support_count}
    """

    # efficient-apriori requires list of tuples or lists
    transactions = [tuple(t) for t in transactions]
    num_trans = len(transactions)

    # Convert min_support (count) → fraction (library uses percentages)
    min_support_fraction = min_support / num_trans

    # Run Apriori from the library
    itemsets, _ = apriori(
        transactions,
        min_support=min_support_fraction,
        min_confidence=0.0,  # we do not need rules
    )

    # Convert itemsets from library format into your format
    L = []
    support_data = {}

    # itemsets is dict: {1: {(item): count}, 2: {(item1,item2):count}, ...}
    for k in sorted(itemsets.keys()):
        level_itemsets = []

        for itemset, support in itemsets[k].items():
            fs = frozenset(itemset)
            level_itemsets.append(fs)
            support_data[fs] = support

        L.append(level_itemsets)

    return L, support_data
