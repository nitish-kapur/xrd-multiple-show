"""
XRD Plotter from CSV (Multiple Show)
Copyright (C) 2026 Nitish Kapur
GitHub: github.com/nitish-kapur
Licensed under GNU GPLv3

    This script was made as a part of a biofuel research project.

    1.  Scans the input folder for all CSV files exported from an XRD
        instrument. Update the desktop_path and input_folder variables
        at the top of the script to match your directory structure.

    2.  For each CSV file, reads all lines and locates the [Scan points]
        section marker to identify where the diffraction data begins. All
        metadata lines above [Scan points] (instrument name, date,
        settings, etc.) are automatically ignored. Files without this
        marker are skipped.

    3.  Expected data format after the [Scan points] marker:

            ... (metadata — instrument name, date, settings, etc.) ...
            [Scan points]
            0.020, 0.5, 123.0
            0.040, 0.5, 145.0
            ...     ...    ...
            
            i.e.,
                Element         Description
                -----------     --------------------------------------------------
                Column 1        2-Theta angle (°) — numeric float
                Column 2        Time per step — read but not plotted
                Column 3        Intensity (counts) — numeric float
                Separator       Comma (,)
                Empty lines     Skipped automatically
                Malformed lines Skipped with a console warning

    4.  Loads the parsed data into a pandas DataFrame and generates a
        matplotlib line plot for each file with:
            - X-axis: 2-Theta (°)
            - Y-axis: Intensity (counts)
            - Title: derived from the CSV filename

    5.  Each plot is displayed non-blocking so the loop continues
        processing remaining files without interruption.

    6.  All plots are kept open together at the end using a final
        plt.show() call. Plots are NOT saved to disk.

    7.  Reports the number of successfully processed files to the console
        upon completion.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Input path ---
desktop_path = r"F:"
input_folder = os.path.join(desktop_path, "raw")

files_processed = 0

for filename in sorted(os.listdir(input_folder)):
    if filename.lower().endswith(".csv"):
        print(f"Processing file: {filename}")
        file_path = os.path.join(input_folder, filename)

        # Read the entire file as lines
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Find the start of the [Scan points] section (case-insensitive)
        data_start_index = None
        for i, line in enumerate(lines):
            if "[scan points]" in line.lower():
                data_start_index = i + 1
                break

        if data_start_index is None:
            print(f"No [Scan points] section found in {filename}, skipping.")
            continue

        # Extract scan points data lines
        data_lines = lines[data_start_index:]

        parsed_data = []
        for line in data_lines:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            parts = line.split(',')
            # At least 3 columns (Angle, TimePerStep, Intensity) are expected
            if len(parts) >= 3:
                try:
                    angle = float(parts[0].strip())
                    intensity = float(parts[2].strip())
                    parsed_data.append([angle, intensity])
                except ValueError:
                    print(f"Skipping non-numeric line in {filename}: {line}")
            else:
                print(f"Skipping malformed line in {filename}: {line}")

        if not parsed_data:
            print(f"No valid XRD data found in {filename}, skipping.")
            continue

        files_processed += 1

        # Create DataFrame for plotting
        df = pd.DataFrame(parsed_data, columns=["Angle", "Intensity"])

        # Prepare plot
        plt.figure(figsize=(10, 5))
        plt.plot(df["Angle"], df["Intensity"], color='blue', linewidth=1)
        plt.title(f"{os.path.splitext(filename)[0]} - XRD Pattern")
        plt.xlabel("2 Theta (°)")
        plt.ylabel("Intensity (counts)")
        plt.grid(True)
        plt.tight_layout()

        # Show plot non-blocking so the loop continues to next file
        plt.show(block=False)

if files_processed == 0:
    print("No CSV files found or no valid XRD data processed.")
else:
    print(f"Processed and plotted XRD data for {files_processed} files.")
    # Keep all plots open until user closes them
    plt.show()
