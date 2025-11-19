import pandas as pd
import matplotlib.pyplot as plt
import re
import glob
import os

# --- 1. Loop through all CSV files in folder ---
csv_files = glob.glob("*.csv")   # adjust path if needed

for filename in csv_files:
    print(f"Processing: {filename}")

    # Load file
    df = pd.read_csv(filename)

    # --- 2. Extract title from filename ---
    match = re.search(r"T\d+\.\w+\.\w+", filename)
    title = match.group(0) if match else "Plot"

    # --- 3. Plot line chart ---
    plt.figure(figsize=(10, 6))

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(
            subset["support_percent"], 
            subset["runtime_seconds"], 
            marker="o", 
            label=algo
        )

    plt.title(f"Runtime vs Support Percent ({title})")
    plt.xlabel("support percent (%)")
    plt.ylabel("runtime (s)")
    plt.legend()
    plt.grid(True)
    plt.gca().invert_xaxis()   # reverse horizontal axis
    plt.tight_layout()

    # Optional: save to file instead of showing each
    outname = f"{title}_runtime_plot.png"
    plt.savefig(outname, dpi=150)
    plt.close()

    print(f"Saved plot: {outname}")
