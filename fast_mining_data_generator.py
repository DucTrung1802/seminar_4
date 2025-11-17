"""
Synthetic T*.I*.D* dataset generator with auto-naming.

Auto filename: T{T_mean}.I{I_mean}.D{D}.txt
Example: T5.I2.D100000.txt
"""

import random
import math


def sample_size(mean, min_v=1, max_v=None):
    if mean <= 10:
        L = math.exp(-mean)
        k, p = 0, 1.0
        while True:
            k += 1
            p *= random.random()
            if p <= L:
                break
        val = max(min_v, k - 1)
    else:
        val = int(max(min_v, random.gauss(mean, math.sqrt(mean))))
    if max_v is not None:
        val = min(max_v, val)
    return val


def generate_maximal_itemsets(N=1000, L=2000, I_mean=2, max_itemset_size=20, seed=None):
    if seed is not None:
        random.seed(seed)
    maximal_sets = []
    for _ in range(L):
        size = sample_size(I_mean, min_v=1, max_v=max_itemset_size)
        items = set(random.sample(range(N), k=min(size, N)))
        maximal_sets.append(tuple(sorted(items)))
    return maximal_sets


def generate_transactions(
    D=100000,
    T_mean=5,
    maximal_sets=None,
    N=1000,
    noise_prob=0.02,
    txn_size_max=50,
    seed=None,
):
    if seed is not None:
        random.seed(seed + 9999)
    if not maximal_sets:
        raise ValueError("maximal_sets must not be empty.")

    transactions = []
    L = len(maximal_sets)

    for _ in range(D):
        target = sample_size(T_mean, min_v=1, max_v=txn_size_max)
        txn_items = set()

        k_sets = 1 if random.random() < 0.8 else (2 if random.random() < 0.9 else 3)
        for _ in range(k_sets):
            txn_items.update(maximal_sets[random.randrange(L)])
            if len(txn_items) >= target:
                break

        attempts = 0
        while len(txn_items) < target and attempts < 5:
            txn_items.update(maximal_sets[random.randrange(L)])
            attempts += 1

        while len(txn_items) < target:
            txn_items.add(random.randrange(N))

        if random.random() < 0.1 and len(txn_items) > 1:
            txn_items.discard(random.choice(list(txn_items)))

        if random.random() < noise_prob:
            for _ in range(random.randint(1, 2)):
                txn_items.add(random.randrange(N))

        if len(txn_items) > txn_size_max:
            txn_items = set(random.sample(list(txn_items), txn_size_max))

        transactions.append(sorted(txn_items))

    return transactions


def auto_filename(T_mean, I_mean, D, N=None, L=None, include_NL=False):
    """Generate filename using K, M, G units for D."""

    def scale_value(x):
        # G (>= 1 billion)
        if x >= 1_000_000_000:
            return format_unit(x, 1_000_000_000, "G")
        # M (>= 1 million)
        elif x >= 1_000_000:
            return format_unit(x, 1_000_000, "M")
        # K (>= 1 thousand)
        elif x >= 1_000:
            return format_unit(x, 1_000, "K")
        # no unit
        else:
            return str(x)

    def format_unit(x, unit_size, unit_label):
        value = x / unit_size
        # If integer (e.g. 1000000/1000000 = 1), show without decimals
        if value.is_integer():
            return f"{int(value)}{unit_label}"
        else:
            return f"{round(value, 1)}{unit_label}"

    D_str = scale_value(D)

    base = f"T{T_mean}.I{I_mean}.D{D_str}"

    if include_NL:
        base += f".N{N}.L{L}"

    return base + ".txt"


def write_transactions(transactions, filename):
    with open(filename, "w") as f:
        for txn in transactions:
            f.write(" ".join(map(str, txn)) + "\n")


if __name__ == "__main__":
    # --- PARAMETERS ---
    N = 1000
    L = 2000
    I_mean = 4
    T_mean = 20
    D = 100_000
    seed = 42
    include_NL_in_filename = False  # optional

    filename = auto_filename(T_mean, I_mean, D, N, L, include_NL=include_NL_in_filename)
    print("Output will be saved as:", filename)

    print("Generating maximal itemsets...")
    maximal_sets = generate_maximal_itemsets(N=N, L=L, I_mean=I_mean, seed=seed)

    print("Generating transactions...")
    transactions = generate_transactions(
        D=D, T_mean=T_mean, maximal_sets=maximal_sets, N=N, seed=seed
    )

    print("Writing file...")
    write_transactions(transactions, filename)
    print("Done.")
