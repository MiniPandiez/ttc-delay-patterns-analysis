from __future__ import annotations

import argparse
from pathlib import Path

from src.analysis import summarize_delay_patterns
from src.preprocess import load_and_clean_dataset
from src.visualize import generate_visualizations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze TTC delay patterns from raw transit delay logs."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/ttc_delay_logs.csv",
        help="Path to the TTC delay CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Directory where generated plots and reports are saved.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at '{input_path}'. "
            "Generate one with: python data/generate_ttc_dataset.py"
        )

    df = load_and_clean_dataset(input_path)
    summary = summarize_delay_patterns(df)

    print("\nTTC Delay Analysis Summary")
    print("=" * 32)
    print(f"Rows analyzed: {len(df):,}")
    print(f"Average delay: {summary['average_delay_minutes']:.2f} minutes")
    print(f"Median delay: {summary['median_delay_minutes']:.2f} minutes")
    print(f"Peak delay hour: {summary['peak_delay_hour']}")
    print(f"Peak hour average: {summary['peak_delay_hour_avg']:.2f} minutes")
    print(f"Most delayed route: {summary['top_route']} ({summary['top_route_delay']:.2f} min avg)")
    print(f"Most reported location: {summary['top_location']} ({summary['top_location_count']} records)")
    print()

    generate_visualizations(df, output_dir)
    print(f"Saved plots to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
