import time
import csv

from apriori import apriori
from setm import SETM
from apriori_tid import apriori_tid
from apriori_hybrid import apriori_hybrid


# ----------------------------------------------------
# Load transactions
# ----------------------------------------------------
def load_transactions(path):
    transactions = []
    with open(path) as f:
        for line in f:
            items = list(map(int, line.strip().split()))
            transactions.append(items)
    return transactions


# ----------------------------------------------------
# Benchmark utility
# ----------------------------------------------------
def benchmark(algorithm_fn, *args):
    start = time.time()
    result = algorithm_fn(*args)
    end = time.time()
    return result, end - start


# ----------------------------------------------------
# Main
# ----------------------------------------------------
if __name__ == "__main__":

    DATAFILE = "T5.I2.D100K.txt"

    # Algorithms to test
    ALGORITHM_LIST = ["apriori", "setm", "apriori_tid", "apriori_hybrid"]

    # Percent supports to test
    MIN_SUPPORT_PERCENT_LIST = [
        0.0025,  # 0.25%
        0.0033,  # 0.33%
        0.005,  # 0.5%
        0.0075,  # 0.75%
        0.01,  # 1%
        0.015,  # 1.5%
        0.02,  # 2%
    ]

    print("Loading transactions...")
    transactions = load_transactions(DATAFILE)
    print(f"Loaded {len(transactions)} transactions\n")

    # Convert list values into strings for the file name
    algos_str = "_".join(ALGORITHM_LIST)
    supports_str = "_".join(str(p) for p in MIN_SUPPORT_PERCENT_LIST)

    # Output CSV file name includes dataset, algorithms, supports
    csv_filename = f"benchmark_output_{DATAFILE}_{algos_str}_{supports_str}.csv"
    csvfile = open(csv_filename, "w", newline="")
    writer = csv.writer(csvfile)

    writer.writerow(
        [
            "algorithm",
            "support_percent",
            "min_support",
            "runtime_seconds",
            "num_frequent_itemsets",
        ]
    )

    # ----------------------------------------------------
    # Loop over support % values
    # ----------------------------------------------------
    for pct in MIN_SUPPORT_PERCENT_LIST:
        MIN_SUPPORT = int(pct * len(transactions))
        if MIN_SUPPORT < 1:
            MIN_SUPPORT = 1

        print(f"\n=== Testing support {pct*100:.2f}% (min_support={MIN_SUPPORT}) ===")

        # ----------------------------------------------------
        # Loop over algorithms
        # ----------------------------------------------------
        for algo in ALGORITHM_LIST:

            print(f"Running {algo}...")

            if algo == "apriori":
                (L, support_data), runtime = benchmark(
                    apriori, transactions, MIN_SUPPORT
                )
                num_itemsets = len(support_data)

            elif algo == "setm":
                (L, support_data), runtime = benchmark(SETM, transactions, MIN_SUPPORT)
                num_itemsets = len(support_data)

            elif algo == "apriori_tid":
                (L, support_data), runtime = benchmark(
                    apriori_tid, transactions, MIN_SUPPORT
                )
                num_itemsets = len(support_data)

            elif algo == "apriori_hybrid":
                (L, support_data), runtime = benchmark(
                    apriori_hybrid, transactions, MIN_SUPPORT
                )
                num_itemsets = len(support_data)

            else:
                print(f"Unknown algorithm: {algo}")
                continue

            print(f"{algo} finished in {runtime:.4f} sec ({num_itemsets} itemsets)")

            # Write one row to CSV file
            writer.writerow([algo, pct * 100, MIN_SUPPORT, runtime, num_itemsets])

    csvfile.close()
    print(f"\nBenchmark complete. Results saved to: {csv_filename}")
