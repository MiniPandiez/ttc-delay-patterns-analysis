from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


def generate_ttc_delay_dataset(output_path: str | Path, n_rows: int = 120000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    start_date = pd.Timestamp("2023-01-01")
    day_offsets = rng.integers(0, 365 * 2, size=n_rows)
    dates = start_date + pd.to_timedelta(day_offsets, unit="D")

    hours = np.concatenate([
        rng.integers(6, 10, size=int(n_rows * 0.22)),
        rng.integers(15, 19, size=int(n_rows * 0.28)),
        rng.integers(0, 24, size=n_rows - int(n_rows * 0.22) - int(n_rows * 0.28)),
    ])
    hours = hours[:n_rows]
    rng.shuffle(hours)

    minutes = rng.integers(0, 60, size=n_rows)
    times = pd.to_datetime(hours * 3600 + minutes * 60, unit="s").dt.strftime("%H:%M:%S")

    routes = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "11", "12", "14", "20", "22", "30", "32", "41", "43", "51",
        "52", "54", "61", "63", "65", "66", "67", "70", "75", "80"
    ]

    locations = [
        "Downtown Station", "Union Station", "St. Clair West", "Jane Station",
        "Bloor-Yonge", "Scarborough Centre", "North York Centre", "King Station",
        "Roncesvalles", "Spadina Station", "Eglinton West", "Keele Station",
        "Dundas West", "Islington Station", "Old Mill", "Warden Station",
        "Kennedy Station", "Sheppard West", "Main Street", "Broadview Station"
    ]

    route_weights = np.array([
        0.08, 0.06, 0.09, 0.07, 0.05, 0.04, 0.03, 0.02, 0.04, 0.05,
        0.04, 0.05, 0.06, 0.03, 0.04, 0.03, 0.02, 0.04, 0.03, 0.05,
        0.04, 0.05, 0.06, 0.04, 0.03, 0.02, 0.04, 0.03, 0.05, 0.04,
    ], dtype=float)
    route_weights = route_weights / route_weights.sum()

    route_assignments = rng.choice(routes, size=n_rows, p=route_weights)

    location_assignments = []
    for route in route_assignments:
        if route in {"1", "2", "3", "5", "7", "9", "11", "14", "30", "41", "51", "61", "75"}:
            loc_pool = ["Downtown Station", "Union Station", "Bloor-Yonge", "King Station", "Spadina Station", "Dundas West"]
        elif route in {"4", "8", "20", "22", "43", "52", "54", "63", "65", "66", "67", "70", "80"}:
            loc_pool = ["Scarborough Centre", "North York Centre", "Kennedy Station", "Warden Station", "Jane Station", "Eglinton West"]
        else:
            loc_pool = locations
        location_assignments.append(rng.choice(loc_pool))
    location_assignments = np.array(location_assignments)

    peak_period_mask = np.isin(hours, np.arange(6, 10)).astype(int) | np.isin(hours, np.arange(15, 19)).astype(int)
    off_peak_mask = 1 - peak_period_mask

    delay_minutes = (
        rng.integers(2, 12, size=n_rows) * (0.7 + 0.8 * peak_period_mask)
        + rng.integers(0, 20, size=n_rows) * (0.4 + 0.8 * off_peak_mask)
        + rng.normal(0, 5, size=n_rows)
    )

    delay_minutes = np.clip(delay_minutes, 1, 90).round(1)

    incident_type = rng.choice(
        ["Signal Delay", "Passenger Activity", "Mechanical Issue", "Weather", "Track Blockage", "Vehicle Breakdown", "Crowding", "Road Work"],
        size=n_rows,
        p=[0.22, 0.18, 0.14, 0.10, 0.12, 0.08, 0.10, 0.06],
    )

    weekday = dates.day_name()
    holiday_adjustment = np.where(
        weekday.isin(["Saturday", "Sunday"]),
        0.85,
        1.0,
    )
    delay_minutes = delay_minutes * holiday_adjustment.to_numpy()

    route_delay_boost = np.array([
        1.25 if route in {"1", "2", "3", "5", "7", "9", "30", "41", "61", "75"} else 1.0
        for route in route_assignments
    ])
    delay_minutes = delay_minutes * route_delay_boost

    delay_minutes = np.clip(delay_minutes, 1, 90).round(1)

    date_strings = dates.dt.strftime("%Y-%m-%d")
    data = pd.DataFrame({
        "date": date_strings,
        "time": times,
        "route": route_assignments,
        "location": location_assignments,
        "delay_minutes": delay_minutes,
        "incident_type": incident_type,
    })

    data = data.sort_values(["date", "time"]).reset_index(drop=True)
    data.to_csv(output_path, index=False)
    return data


if __name__ == "__main__":
    dataset = generate_ttc_delay_dataset("data/ttc_delay_logs.csv", n_rows=120000)
    print(f"Generated synthetic TTC delay dataset with {len(dataset):,} rows at data/ttc_delay_logs.csv")
