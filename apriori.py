from efficient_apriori import apriori


def apriori_efficient(transactions, min_support=2):
    """
    Wrapper around the efficient-apriori library
    to match the structure of your previous Apriori function.

    Input:
        transactions: list of lists/sets of items
        min_support: integer support threshold (count, not fraction)

    Output:
        L: list of dicts ({frozenset: support_count}) by level
        support_data: dict of all frequent itemsets with support counts
    """

    # Convert integer min_support (count) to fraction for the library
    min_support_fraction = min_support / len(transactions)

    # Run Apriori from library
    itemsets, _ = apriori(
        transactions,
        min_support=min_support_fraction,
        min_confidence=0.0,  # confidence not needed
    )

    # Reform into your desired output format:
    # L = [{frozenset: count}, {frozenset: count}, ...]
    L = []
    support_data = {}

    for k in sorted(itemsets.keys()):
        level_dict = {}
        for itemset, support in itemsets[k].items():
            level_dict[frozenset(itemset)] = support
            support_data[frozenset(itemset)] = support
        L.append(level_dict)

    return L, support_data
