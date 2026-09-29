from __future__ import annotations

import pandas as pd


def summarize_delay_patterns(df: pd.DataFrame):
    """Return key statistics from TTC delay data."""
    summary = {
        "total_records": int(len(df)),
        "average_delay_minutes": float(df["delay_minutes"].mean()),
        "median_delay_minutes": float(df["delay_minutes"].median()),
        "max_delay_minutes": float(df["delay_minutes"].max()),
    }

    hourly = df.groupby("hour")["delay_minutes"].mean().sort_values(ascending=False)
    summary["peak_delay_hour"] = int(hourly.index[0]) if not hourly.empty else None
    summary["peak_delay_hour_avg"] = float(hourly.iloc[0]) if not hourly.empty else 0.0

    route_summary = df.groupby("route", dropna=False)["delay_minutes"].mean().sort_values(ascending=False)
    summary["top_route"] = route_summary.index[0] if not route_summary.empty else "N/A"
    summary["top_route_delay"] = float(route_summary.iloc[0]) if not route_summary.empty else 0.0

    location_summary = df["location"].dropna().value_counts()
    summary["top_location"] = location_summary.index[0] if not location_summary.empty else "N/A"
    summary["top_location_count"] = int(location_summary.iloc[0]) if not location_summary.empty else 0

    return summary


def compute_time_series_metrics(df: pd.DataFrame):
    """Compute group-by time metrics for trend analysis."""
    hourly_delay = (
        df.groupby("hour", as_index=False)["delay_minutes"]
        .agg(["mean", "median", "count"])
        .rename(columns={"mean": "avg_delay_minutes", "median": "median_delay_minutes", "count": "record_count"})
        .sort_values("hour")
    )

    daily_delay = (
        df.groupby("day_of_week", as_index=False)["delay_minutes"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "avg_delay_minutes", "count": "record_count"})
        .sort_values("avg_delay_minutes", ascending=False)
    )

    route_delay = (
        df.groupby("route", dropna=False, as_index=False)["delay_minutes"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "avg_delay_minutes", "count": "record_count"})
        .sort_values("avg_delay_minutes", ascending=False)
    )

    location_delay = (
        df.groupby("location", dropna=False, as_index=False)["delay_minutes"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "avg_delay_minutes", "count": "record_count"})
        .sort_values("avg_delay_minutes", ascending=False)
    )

    return {
        "hourly_delay": hourly_delay,
        "daily_delay": daily_delay,
        "route_delay": route_delay,
        "location_delay": location_delay,
    }
