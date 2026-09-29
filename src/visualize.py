from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.analysis import compute_time_series_metrics


sns.set_theme(style="whitegrid")


def generate_visualizations(df: pd.DataFrame, output_dir: str | Path):
    """Create delay-pattern charts for the TTC analysis project."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    metrics = compute_time_series_metrics(df)
    hourly = metrics["hourly_delay"]
    daily = metrics["daily_delay"]
    route = metrics["route_delay"].head(10)
    location = metrics["location_delay"].head(10)

    day_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    daily_plot = daily.copy()
    daily_plot["day_of_week"] = pd.Categorical(daily_plot["day_of_week"], categories=day_order, ordered=True)
    daily_plot = daily_plot.sort_values("day_of_week").reset_index(drop=True)

    plt.figure(figsize=(10, 6))
    plt.plot(hourly["hour"], hourly["avg_delay_minutes"], color="#1f77b4", marker="o", linewidth=2)
    plt.title("Average Delay by Hour of Day")
    plt.xlabel("Hour")
    plt.ylabel("Average Delay (minutes)")
    plt.grid(alpha=0.35)
    plt.tight_layout()
    plt.savefig(output_path / "average_delay_by_hour.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=daily_plot, x="day_of_week", y="avg_delay_minutes", palette="Blues_d")
    plt.title("Average Delay by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Delay (minutes)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_path / "delay_by_day_of_week.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=route, y="route", x="avg_delay_minutes", palette="Oranges_r", orient="h")
    plt.title("Top Routes by Average Delay")
    plt.xlabel("Average Delay (minutes)")
    plt.ylabel("Route")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path / "top_routes_by_delay.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=location, y="location", x="avg_delay_minutes", palette="Greens_r", orient="h")
    plt.title("Top Locations by Average Delay")
    plt.xlabel("Average Delay (minutes)")
    plt.ylabel("Location")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path / "top_locations_by_delay.png", dpi=200)
    plt.close()

    print(f"Generated plots in {output_path.resolve()}")
