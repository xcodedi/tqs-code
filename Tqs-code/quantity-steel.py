import os
import re
from collections import defaultdict


os.system('cls' if os.name == 'nt' else 'clear')


FOLDER = r"folder" 
VALID_GAUGES = {5, 6.3, 8, 10, 12.5, 16, 20, 25} 


SUMMARY_LINE = re.compile(
    r'^\s*(50A|60A)\s+(\d+(?:[.,]\d+)?)\s+(\d+(?:[.,]\d+)?)\s+(\d+(?:[.,]\d+)?)\s*$'
)

def parse_num(s: str) -> float | None:
    """Convert string number with different decimal separators to float"""
    t = s.strip()
    if "," in t and "." in t:
        # Handle cases like "1.234,56" by removing thousand separators first
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None

def process_lst(file_path: str):
    """Process a .LST file and return sums by gauge and steel type"""
    lines = None
    for encoding in ("cp1252", "latin-1", "utf-8"):
        try:
            lines = open(file_path, "r", encoding=encoding, errors="ignore").read().splitlines()
            break
        except Exception:
            lines = None

    if lines is None:
        print(f"Could not read file: {file_path}")
        return {}, {}

    sum_by_gauge = defaultdict(float)
    sum_by_steel = defaultdict(float)

    for line in lines:
        # Skip lines containing "peso total" (total weight)
        if "peso total" in line.lower():
            continue

        m = SUMMARY_LINE.match(line)
        if not m:
            continue

        steel_type, gauge_str, length_str, weight_str = m.groups()
        gauge = parse_num(gauge_str)
        weight = parse_num(weight_str)

        # Skip invalid entries
        if gauge is None or weight is None or gauge not in VALID_GAUGES:
            continue

        # Accumulate weights
        sum_by_gauge[gauge] += weight
        sum_by_steel[steel_type] += weight

    return sum_by_gauge, sum_by_steel


total_by_gauge = defaultdict(float)
total_by_steel = defaultdict(float)

files = [f for f in os.listdir(FOLDER) if f.lower().endswith(".lst")]
if not files:
    print("No .LST files found in folder. Please check FOLDER path.")
else:
    for filename in files:
        path = os.path.join(FOLDER, filename)
        file_sum_gauge, file_sum_steel = process_lst(path)

        print(f"\n📄 {filename}")
        if not file_sum_gauge:
            print("  (no valid lines in STEEL SUMMARY section)")
        else:
            for gauge in sorted(file_sum_gauge):
                print(f"  Gauge {gauge:g} mm: {file_sum_gauge[gauge]:.2f} kgf")

        # Accumulate to totals
        for gauge, v in file_sum_gauge.items():
            total_by_gauge[gauge] += v
        for steel, v in file_sum_steel.items():
            total_by_steel[steel] += v

    # Print final reports
    print("\n📊 GRAND TOTAL (all sheets) — by gauge:")
    for gauge in sorted(total_by_gauge):
        print(f"  Gauge {gauge:g} mm: {total_by_gauge[gauge]:.2f} kgf")

    print("\n🔎 Totals by STEEL TYPE (optional):")
    for steel_type in ("50A", "60A"):
        if steel_type in total_by_steel:
            print(f"  {steel_type}: {total_by_steel[steel_type]:.2f} kgf")