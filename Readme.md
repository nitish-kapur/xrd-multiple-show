# XRD Plotter from CSV (Multiple Show)

A Python script that batch processes XRD diffraction patterns from CSV files and displays all plots simultaneously in interactive matplotlib windows.

## Author

**Nitish Kapur**<br>
GitHub: [github.com/nitish-kapur](https://github.com/nitish-kapur)

## Expected Input Format

The script expects CSV files exported from an XRD instrument. Each file must contain a `[Scan points]` section marker, after which the diffraction data begins in at least three comma-separated columns:

    ... (metadata — instrument name, date, settings, etc.) ...
    [Scan points]
    0.020, 0.5, 123.0
    0.040, 0.5, 145.0
    0.060, 0.5, 132.0
    ...

| Element | Description |
|---|---|
| Metadata lines | Any number of lines before `[Scan points]` — automatically ignored by the parser |
| `[Scan points]` marker | Signals the end of metadata; data parsing begins on the next line |
| Column 1 | 2-Theta angle (°) — must be a numeric float |
| Column 2 | Time per step — read but not plotted |
| Column 3 | Intensity (counts) — must be a numeric float |
| Separator | Comma (`,`) |
| Empty lines | Skipped automatically |
| Malformed lines | Lines with fewer than three values are skipped with a console warning |

## Requirements

    pip install pandas matplotlib

## Configuration

The input folder path is hard-coded at the top of the script. Update it to match your directory structure:

    desktop_path = r"F:"
    input_folder = os.path.join(desktop_path, "raw")

## Usage

1. Place all XRD CSV files in the input folder
2. Run:

    python xrd-multiple-show.py

All plots are displayed simultaneously in interactive matplotlib windows once all files have been processed.

## Output

- One interactive matplotlib window per CSV file
- X-axis: 2-Theta (°)
- Y-axis: Intensity (counts)
- Title: derived from the CSV filename

## Notes

- Unlike a save version, plots are displayed interactively and are NOT saved to disk.
- Files that do not contain a `[Scan points]` marker or have no valid data are skipped automatically.
- All plots are non-blocking during processing and are kept open together at the end using a final `plt.show()` call.
