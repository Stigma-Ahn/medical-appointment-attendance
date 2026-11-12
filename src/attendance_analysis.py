"""Reproducible descriptive medical appointment attendance analysis.

Does not establish causation, treatment efficacy or individual patient risk.
Requires an authorized locally held CSV.
"""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED = {
    "PatientId", "AppointmentID", "Gender", "ScheduledDay", "AppointmentDay",
    "Age", "Neighbourhood", "Scholarship", "Hipertension", "Diabetes",
    "Alcoholism", "Handcap", "SMS_received", "No-show",
}
BINS = [-1, 0, 7, 14, 30, float("inf")]
LABELS = ["0", "1-7", "8-14", "15-30", "31+"]
AGE_BINS = [-1, 17, 39, 64, float("inf")]
AGE_LABELS = ["0-17", "18-39", "40-64", "65+"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_and_validate(path: Path) -> tuple[pd.DataFrame, dict]:
    # Treat identifiers as labels rather than floating point quantities.
    raw = pd.read_csv(path, dtype={"PatientId": "string", "AppointmentID": "string"})
    missing = sorted(REQUIRED - set(raw.columns))
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {missing}")

    df = raw.copy()
    outcomes = df["No-show"].astype("string").str.strip().str.lower()
    df["no_show"] = outcomes.map({"yes": 1, "no": 0})
    df["age_num"] = pd.to_numeric(df["Age"], errors="coerce")
    df["scheduled_dt"] = pd.to_datetime(df["ScheduledDay"], errors="coerce", utc=True)
    df["appointment_dt"] = pd.to_datetime(df["AppointmentDay"], errors="coerce", utc=True)

    # Use calendar-date differences; booking timestamps and midnight
    # appointment timestamps should not make same-day leads negative.
    df["lead_days"] = (
        df["appointment_dt"].dt.normalize() - df["scheduled_dt"].dt.normalize()
    ).dt.days

    checks = {
        "source_path": str(path),
        "source_sha256": sha256_file(path),
        "raw_rows": int(len(raw)),
        "raw_columns": int(len(raw.columns)),
        "duplicate_appointment_id_rows": int(df["AppointmentID"].duplicated(keep=False).sum()),
        "distinct_patient_ids": int(df["PatientId"].nunique(dropna=True)),
        "patients_with_multiple_rows": int((df.groupby("PatientId", dropna=True).size() > 1).sum()),
        "missing_outcome_or_unknown_label": int(df["no_show"].isna().sum()),
        "missing_or_invalid_dates": int((df["scheduled_dt"].isna() | df["appointment_dt"].isna()).sum()),
        "negative_lead_days": int((df["lead_days"] < 0).sum()),
        "missing_or_negative_age": int((df["age_num"].isna() | (df["age_num"] < 0)).sum()),
        "age_over_115_flag_review": int((df["age_num"] > 115).sum()),
        "sms_unique_values": sorted(df["SMS_received"].astype("string").dropna().unique().tolist()),
        "outcome_unique_values": sorted(outcomes.dropna().unique().tolist()),
        "column_names": list(raw.columns),
        "missing_by_source_column": {str(k): int(v) for k, v in raw.isna().sum().to_dict().items()},
    }

    bad_outcome = df["no_show"].isna()
    bad_dates = df["scheduled_dt"].isna() | df["appointment_dt"].isna()
    negative_lead = df["lead_days"] < 0
    invalid_age = df["age_num"].isna() | (df["age_num"] < 0)
    excluded = bad_outcome | bad_dates | negative_lead | invalid_age
    checks["excluded_any_reason"] = int(excluded.sum())
    checks["included_rows"] = int((~excluded).sum())
    checks["exclusions_may_overlap"] = True
    checks["data_scope"] = "appointment records, not independent unique patients"
    checks["sms_interpretation"] = "observational association only; no randomized effect claim"
    checks["findings_status"] = "local descriptive analysis; needs researcher verification"

    analysis = df.loc[~excluded].copy()
    analysis["lead_group"] = pd.cut(analysis["lead_days"], bins=BINS, labels=LABELS)
    analysis["age_group"] = pd.cut(analysis["age_num"], bins=AGE_BINS, labels=AGE_LABELS)
    return analysis, checks


def summarize_rates(df: pd.DataFrame, column: str) -> pd.DataFrame:
    result = (
        df.groupby(column, observed=True)["no_show"]
        .agg(appointments="size", missed="sum", miss_rate="mean")
        .reset_index()
    )
    result["miss_rate_percent"] = (result["miss_rate"] * 100).round(2)
    return result


def run(input_path: Path, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    df, quality = read_and_validate(input_path)
    with (output / "quality_report.json").open("w", encoding="utf-8") as f:
        json.dump(quality, f, ensure_ascii=False, indent=2)
    if df.empty:
        raise ValueError("No usable rows; inspect quality_report.json")

    overall = {
        "included_appointments": int(len(df)),
        "missed_appointments": int(df["no_show"].sum()),
        "no_show_percentage": round(float(df["no_show"].mean()) * 100, 2),
    }
    with (output / "overall_summary.json").open("w", encoding="utf-8") as f:
        json.dump(overall, f, indent=2)

    by_lead = summarize_rates(df, "lead_group")
    by_age = summarize_rates(df, "age_group")
    by_sms = summarize_rates(df, "SMS_received")
    by_lead.to_csv(output / "lead_time_rates.csv", index=False)
    by_age.to_csv(output / "age_group_rates.csv", index=False)
    by_sms.to_csv(output / "sms_status_rates.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4.7))
    ax.bar(by_lead["lead_group"].astype(str), by_lead["miss_rate_percent"])
    ax.set_xlabel("Booking-to-appointment lead time (calendar days)")
    ax.set_ylabel("Observed no-show rate (%)")
    ax.set_title("Descriptive association, not a causal effect")
    fig.tight_layout()
    fig.savefig(output / "lead_time_rates.png", dpi=160)
    plt.close(fig)
    return {**quality, **overall}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Locally held Kaggle CSV")
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    result = run(args.input, args.output)
    print(json.dumps({k: result[k] for k in [
        "raw_rows", "included_rows", "excluded_any_reason", "source_sha256",
        "no_show_percentage"]}, indent=2))
    print("Check quality_report.json and confirm assumptions before reporting findings.")


if __name__ == "__main__":
    main()
