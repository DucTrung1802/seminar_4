import pandas as pd
import matplotlib.pyplot as plt
import re
import glob
import os

# --- 1. Loop through all CSV files in folder ---
csv_files = glob.glob("*.csv")  # adjust path if needed

for filename in csv_files:
    print(f"\nProcessing: {filename}")

    # ----------------------------------------------------
    # Try loading the CSV
    # ----------------------------------------------------
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"❌ Failed to load {filename}: {e}")
        continue

    # Required columns check
    required_cols = {"algorithm", "support_percent", "runtime_seconds"}
    if not required_cols.issubset(df.columns):
        print(f"❌ Missing required columns in {filename}. Skipping.")
        continue

    # ----------------------------------------------------
    # Extract title from filename (T?.I?.D?.S?)
    # ----------------------------------------------------
    try:
        match = re.search(r"(T\d+\.I\d+\.D\w+\.S\d+)", filename)
        title = match.group(1) if match else "Plot"
    except Exception as e:
        print(f"❌ Title extraction error for {filename}: {e}")
        continue

    # ----------------------------------------------------
    # Plot the line chart
    # ----------------------------------------------------
    try:
        plt.figure(figsize=(10, 6))

        for algo in df["algorithm"].unique():
            subset = df[df["algorithm"] == algo]
            plt.plot(
                subset["support_percent"],
                subset["runtime_seconds"],
                marker="o",
                label=algo,
            )

        plt.title(f"Runtime vs Support Percent ({title.split('.')[:-1]})")
        plt.xlabel("support percent (%)")
        plt.ylabel("runtime (s)")
        plt.legend()
        plt.grid(True)
        plt.gca().invert_xaxis()
        plt.tight_layout()

        # Save output
        outname = f"{title}_runtime_plot.png"
        plt.savefig(outname, dpi=150)
        plt.close()

        print(f"✅ Saved plot: {outname}")

    except Exception as e:
        print(f"❌ Plotting failed for {filename}: {e}")
        continue
