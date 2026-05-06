#!/usr/bin/env python3
"""
Fetch latest Global Carbon Project fossil CO2 data and update global.csv and data/fuel-breakdown.csv.

Source: Global Carbon Budget (Zenodo)
  Andrew, R. M., & Peters, G. P. (2025). The Global Carbon Project's fossil CO2
  emissions dataset (2025v15). Zenodo. https://doi.org/10.5281/zenodo.17417124

Units:
  global.csv        — million metric tonnes of Carbon (MtC)
  fuel-breakdown.csv — million metric tonnes of CO2 (MtCO2)
"""

import csv
import io
import sys
import urllib.request
from pathlib import Path

# GCP release to fetch — update this URL when a new annual release drops
GCP_URL = "https://zenodo.org/records/17417124/files/GCB2025v15_MtCO2_flat.csv?download=1"

# CO2 → C conversion factor (12/44)
CO2_TO_C = 12 / 44

REPO_ROOT = Path(__file__).parent.parent
GLOBAL_CSV = REPO_ROOT / "global.csv"
FUEL_BREAKDOWN_CSV = REPO_ROOT / "data" / "fuel-breakdown.csv"

# Fuel columns in GCP → display names used in fuel-breakdown.csv
FUEL_COLS = {
    "Coal":    "Solid Fuel",
    "Oil":     "Liquid Fuel",
    "Gas":     "Gas Fuel",
    "Cement":  "Cement",
    "Flaring": "Gas Flaring",
    "Other":   "Other",
}


def fetch_gcp():
    print(f"Fetching {GCP_URL} ...")
    req = urllib.request.Request(GCP_URL, headers={"User-Agent": "datasets/co2-fossil-global"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def parse_global_rows(raw_csv):
    reader = csv.DictReader(io.StringIO(raw_csv))
    rows = []
    for row in reader:
        if row["Country"] != "Global":
            continue
        year = int(row["Year"])

        def val(col):
            v = row.get(col, "").strip()
            return float(v) if v else None

        rows.append({
            "Year":        year,
            "Total_MtCO2": val("Total"),
            "Coal_MtCO2":  val("Coal"),
            "Oil_MtCO2":   val("Oil"),
            "Gas_MtCO2":   val("Gas"),
            "Cement_MtCO2":  val("Cement"),
            "Flaring_MtCO2": val("Flaring"),
            "Other_MtCO2":   val("Other"),
            "PerCapita_tCO2": val("Per Capita"),
        })
    rows.sort(key=lambda r: r["Year"])
    return rows


def fmt(v, decimals=0):
    """Format number or empty string."""
    if v is None:
        return ""
    if decimals == 0:
        return str(round(v))
    return f"{v:.{decimals}f}".rstrip("0").rstrip(".")


def write_global_csv(rows):
    with open(GLOBAL_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Total", "Gas Fuel", "Liquid Fuel", "Solid Fuel",
                         "Cement", "Gas Flaring", "Per Capita"])
        for r in rows:
            def c(v):
                return None if v is None else v * CO2_TO_C

            year = r["Year"]
            total    = fmt(c(r["Total_MtCO2"]))
            gas_fuel = fmt(c(r["Gas_MtCO2"]))
            liq_fuel = fmt(c(r["Oil_MtCO2"]))
            sol_fuel = fmt(c(r["Coal_MtCO2"]))
            cement   = fmt(c(r["Cement_MtCO2"]))
            flaring  = fmt(c(r["Flaring_MtCO2"]))
            # Per capita: tCO2/person → tC/person, 2 decimal places
            pc = r["PerCapita_tCO2"]
            per_cap = fmt(pc * CO2_TO_C, 2) if pc is not None else ""
            writer.writerow([year, total, gas_fuel, liq_fuel, sol_fuel, cement, flaring, per_cap])
    print(f"Wrote {GLOBAL_CSV} ({len(rows)} rows, {rows[0]['Year']}–{rows[-1]['Year']})")


def write_fuel_breakdown_csv(rows):
    with open(FUEL_BREAKDOWN_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["year", "fuel", "emissions_mt"])
        for r in rows:
            for gcp_col, label in FUEL_COLS.items():
                key = f"{gcp_col}_MtCO2"
                v = r.get(key)
                if v is not None:
                    writer.writerow([r["Year"], label, round(v, 1)])
    print(f"Wrote {FUEL_BREAKDOWN_CSV}")


def main():
    raw = fetch_gcp()
    rows = parse_global_rows(raw)
    if not rows:
        print("ERROR: no Global rows found in GCP data", file=sys.stderr)
        sys.exit(1)
    print(f"Found {len(rows)} Global rows ({rows[0]['Year']}–{rows[-1]['Year']})")
    write_global_csv(rows)
    write_fuel_breakdown_csv(rows)
    print("Done.")


if __name__ == "__main__":
    main()
