from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


def normalize_column_names(columns):
    """Normalize raw column names into lowercase snake_case."""
    cleaned = []
    for col in columns:
        value = str(col).strip().lower()
        value = re.sub(r"[^a-z0-9]+", "_", value)
        value = re.sub(r"_+", "_", value).strip("_")
        cleaned.append(value)
    return cleaned


def parse_datetime_column(df: pd.DataFrame, date_col: str, time_col: str | None = None):
    """Create a single datetime series from date and optional time columns."""
    if date_col not in df.columns:
        raise KeyError(f"Date column '{date_col}' not found in dataset.")

    date_values = df[date_col].astype(str)
    if time_col and time_col in df.columns:
        combined = date_values + " " + df[time_col].astype(str)
    else:
        combined = date_values

    return pd.to_datetime(combined, errors="coerce")


def detect_common_columns(df: pd.DataFrame):
    """Map a variety of common TTC column names to canonical names."""
    col_map = {str(c).strip().lower(): c for c in df.columns}

    def find(*choices):
        for choice in choices:
            if choice in col_map:
                return col_map[choice]
        return None

    return {
        "date": find("date", "datetime", "timestamp", "incident_date", "occurred_at", "report_date"),
        "time": find("time", "incident_time", "occurred_time", "time_of_day"),
        "route": find("route", "route_number", "line", "route_name", "vehicle_route"),
        "location": find("location", "stop", "station", "station_name", "stop_name", "place", "area"),
        "delay": find("delay_minutes", "delay_min", "minutes_delay", "delay", "delay_time", "minutes"),
        "type": find("incident_type", "type", "delay_type", "reason", "cause"),
    }


def clean_numeric_series(series: pd.Series):
    """Convert numeric-like text values to floats and replace invalid values with NaN."""
    cleaned = pd.to_numeric(series.astype(str).str.replace(",", "", regex=False), errors="coerce")
    return cleaned


def load_and_clean_dataset(path: str | Path) -> pd.DataFrame:
    """Load the TTC data, normalize fields, and return an analysis-ready DataFrame."""
    csv_path = Path(path)
    df = pd.read_csv(csv_path)
    df.columns = normalize_column_names(df.columns)

    mapping = detect_common_columns(df)
    date_col = mapping["date"]
    if date_col is None:
        raise ValueError("Could not detect a valid date column in the dataset.")

    time_col = mapping["time"]
    route_col = mapping["route"]
    location_col = mapping["location"]
    delay_col = mapping["delay"]
    type_col = mapping["type"]

    df["route"] = df[route_col].astype(str).str.strip() if route_col else pd.NA
    df["location"] = df[location_col].astype(str).str.strip() if location_col else pd.NA
    df["incident_type"] = df[type_col].astype(str).str.strip() if type_col else pd.NA

    df["timestamp"] = parse_datetime_column(df, date_col, time_col)
    df = df.dropna(subset=["timestamp"]).copy()

    if delay_col is not None:
        df["delay_minutes"] = clean_numeric_series(df[delay_col])
    else:
        df["delay_minutes"] = pd.NA

    df["delay_minutes"] = pd.to_numeric(df["delay_minutes"], errors="coerce")
    df["delay_minutes"] = df["delay_minutes"].fillna(0)

    df["route"] = df["route"].replace({"nan": pd.NA, "None": pd.NA})
    df["location"] = df["location"].replace({"nan": pd.NA, "None": pd.NA})
    df["incident_type"] = df["incident_type"].replace({"nan": pd.NA, "None": pd.NA})

    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["hour"] = df["timestamp"].dt.hour
    df["time_bucket"] = df["hour"].apply(
        lambda h: "Late Night" if h < 5 else "Morning" if h < 12 else "Afternoon" if h < 17 else "Evening"
    )

    return df.sort_values("timestamp").reset_index(drop=True)
