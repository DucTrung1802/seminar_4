import time
import csv
import os
import re

from apriori import apriori_efficient
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


def expand_datafiles(regex_list, folder="."):
    """Return list of filenames matching any regex in regex_list."""
    all_files = os.listdir(folder)
    selected = []

    for pattern in regex_list:
        regex = re.compile(pattern)
        for f in all_files:
            if regex.fullmatch(f):
                selected.append(f)

    return sorted(selected)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
if __name__ == "__main__":

    # Now a LIST of files
    DATAFILES = [
        # "T5.I2.D1K.txt",
        # "T5.I2.D100K.txt",
        # "T10.I2.D100K.txt",
        # r"T10\.I4\.D100K\.S.*\.txt",
        # r"T20\.I2\.D100K\.S.*\.txt",
        r"T20\.I4\.D100K\.S.*\.txt",
        # "T20.I6.D100K.txt",
    ]

    # Algorithms to test
    ALGORITHM_LIST = ["setm", "apriori", "apriori_tid", "apriori_hybrid"]

    # Percent supports to test
    MIN_SUPPORT_PERCENT_LIST = [
        0.0025,
        0.0033,
        0.005,
        0.0075,
        0.01,
        0.015,
        0.02,
    ]

    # ----------------------------------------------------
    # Loop over each dataset file
    # ----------------------------------------------------
    matched_files = expand_datafiles(DATAFILES)
    for DATAFILE in matched_files:

        print(f"\n==============================")
        print(f"Loading dataset: {DATAFILE}")
        print(f"==============================")

        transactions = load_transactions(DATAFILE)
        print(f"Loaded {len(transactions)} transactions\n")

        # Convert list values into strings for file name
        algos_str = "_".join(ALGORITHM_LIST)
        supports_str = "_".join(str(p) for p in MIN_SUPPORT_PERCENT_LIST)

        # Extract seed (e.g., S1207)
        seed_match = re.search(r"S(\d+)", DATAFILE)
        seed_suffix = ""
        if seed_match:
            seed_suffix = f"_s{seed_match.group(1)}"

        # Output CSV name includes dataset name + seed
        csv_filename = (
            f"benchmark_output_{DATAFILE}_{algos_str}_{supports_str}{seed_suffix}.csv"
        )

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

            print(
                f"\n=== Testing support {pct*100:.2f}% (min_support={MIN_SUPPORT}) ==="
            )

            # ----------------------------------------------------
            # Loop over algorithms
            # ----------------------------------------------------
            for algo in ALGORITHM_LIST:

                print(f"Running {algo}...")

                if algo == "setm":
                    (L, support_data), runtime = benchmark(
                        SETM, transactions, MIN_SUPPORT
                    )
                    num_itemsets = len(support_data)

                elif algo == "apriori":
                    (L, support_data), runtime = benchmark(
                        apriori_efficient, transactions, MIN_SUPPORT
                    )
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

                # Write results for this dataset
                writer.writerow([algo, pct * 100, MIN_SUPPORT, runtime, num_itemsets])

        csvfile.close()
        print(f"\nBenchmark for {DATAFILE} complete. Saved: {csv_filename}")
