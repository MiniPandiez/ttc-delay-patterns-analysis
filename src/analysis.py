from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


def normalize_column_names(columns):
    """Convert column names to a clean lowercase snake_case form."""
    cleaned = []
    for col in columns:
        value = str(col).strip().lower()
        value = re.sub(r"[^a-z0-9]+", "_", value)
        value = re.sub(r"_+", "_", value).strip("_")
        cleaned.append(value)
    return cleaned


def parse_datetime_column(df: pd.DataFrame, date_col: str, time_col: str | None = None):
    """Create a datetime column from date and optional time columns."""
    if date_col in df.columns:
        date_values = df[date_col].astype(str)
    else:
        raise KeyError(f"Date column '{date_col}' not found in dataset.")

    if time_col and time_col in df.columns:
        time_values = df[time_col].astype(str)
        combined = date_values + " " + time_values
    else:
        combined = date_values

    dt = pd.to_datetime(combined, errors="coerce")
    return dt


def detect_common_columns(df: pd.DataFrame):
    """Match a wide range of possible input column names to canonical names."""
    col_map = {str(c).strip().lower(): c for c in df.columns}

    def find(*choices):
        for choice in choices:
            if choice in col_map:
                return col_map[choice]
        return None

    date_col = find(
        "date",
        "datetime",
        "timestamp",
        "incident_date",
        "occurred_at",
        "report_date",
    )
    time_col = find(
        "time",
        "incident_time",
        "occurred_time",
        "time_of_day",
    )
    route_col = find(
        "route",
        "route_number",
        "line",
        "route_name",
        "vehicle_route",
    )
    location_col = find(
        "location",
        "stop",
        "station",
        "station_name",
        "stop_name",
        "place",
        "area",
    )
    delay_col = find(
        "delay_minutes",
        "delay_min",
        "minutes_delay",
        "delay",
        "delay_time",
        "minutes",
    )
    type_col = find(
        "incident_type",
        "type",
        "delay_type",
        "reason",
        "cause",
    )

    return {"date": date_col, "time": time_col, "route": route_col, "location": location_col, "delay": delay_col, "type": type_col}


def clean_numeric_series(series: pd.Series):
    """Convert numeric-like text values to floats and replace invalid values with NaN."""
    cleaned = pd.to_numeric(series.astype(str).str.replace(",", "", regex=False), errors="coerce")
    return cleaned


def load_and_clean_dataset(path: str | Path) -> pd.DataFrame:
    """Load TTC delay data, normalize columns, and produce a usable analysis-ready DataFrame."""
    csv_path = Path(path)
    df = pd.read_csv(csv_path)

    df.columns = normalize_column_names(df.columns)
    mapping = detect_common_columns(df)

    if mapping["date"] is None:
        raise ValueError(
            "Could not detect a date column. Ensure your CSV contains a date/timestamp field."
        )

    date_col = mapping["date"]
    time_col = mapping["time"]
    route_col = mapping["route"]
    location_col = mapping["location"]
    delay_col = mapping["delay"]
    type_col = mapping["type"]

    if route_col is not None:
        df["route"] = df[route_col].astype(str).str.strip()
        df.loc[df["route"].eq("nan"), "route"] = pd.NA
    else:
        df["route"] = pd.NA

    if location_col is not None:
        df["location"] = df[location_col].astype(str).str.strip()
        df.loc[df["location"].eq("nan"), "location"] = pd.NA
    else:
        df["location"] = pd.NA

    if type_col is not None:
        df["incident_type"] = df[type_col].astype(str).str.strip()
        df.loc[df["incident_type"].eq("nan"), "incident_type"] = pd.NA
    else:
        df["incident_type"] = pd.NA

    df["timestamp"] = parse_datetime_column(df, date_col, time_col)
    df = df.dropna(subset=["timestamp"]).copy()

    if delay_col is not None:
        df["delay_minutes"] = clean_numeric_series(df[delay_col])
    else:
        df["delay_minutes"] = pd.NA

    df["delay_minutes"] = df["delay_minutes"].fillna(df.get("delay_minutes", pd.Series([pd.NA] * len(df))))
    df["delay_minutes"] = pd.to_numeric(df["delay_minutes"], errors="coerce")

    df["delay_minutes"] = df["delay_minutes"].fillna(0)

    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["hour"] = df["timestamp"].dt.hour
    df["time_bucket"] = df["hour"].apply(
        lambda h: "Late Night" if h < 5 else "Morning" if h < 12 else "Afternoon" if h < 17 else "Evening"
    )

    df["route"] = df["route"].replace({"nan": pd.NA, "None": pd.NA})
    df["location"] = df["location"].replace({"nan": pd.NA, "None": pd.NA})
    df["incident_type"] = df["incident_type"].replace({"nan": pd.NA, "None": pd.NA})

    df = df.sort_values("timestamp").reset_index(drop=True)
    return df
