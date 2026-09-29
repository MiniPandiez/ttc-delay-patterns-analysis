# Time-Series Analysis: TTC Delay Patterns

A Python-based transit analytics project that examines TTC delay logs to uncover temporal and spatial congestion patterns using public transportation data.

## Overview
This project analyzes a public dataset containing 100,000+ Toronto Transit Commission (TTC) delay records. The objective is to identify recurring delay trends, understand operational hotspots, and communicate patterns through clear visual analytics.

The workflow emphasizes:
- data cleaning and missing-value handling
- timestamp normalization and feature engineering
- temporal aggregation by hour, day, and month
- route and location analysis
- visual storytelling using Matplotlib and Seaborn

## Project Goals
- Detect delay patterns by time of day and day of week
- Measure average delay severity by route and stop/location
- Identify peak congestion windows and recurring hotspots
- Demonstrate strong Python data wrangling and time-series analysis skills

## Tools Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Repository Structure
```text
.
├── data/
│   └── ttc_delay_logs.csv
├── results/
│   ├── average_delay_by_hour.png
│   ├── delay_by_day_of_week.png
│   ├── top_routes_by_delay.png
│   └── top_locations_by_delay.png
├── src/
│   ├── __init__.py
│   ├── analysis.py
│   ├── preprocess.py
│   └── visualize.py
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── LICENSE
```

## Setup
Clone the project and install the dependencies:

```bash
git clone https://github.com/MiniPandiez/ttc-delay-patterns-analysis.git
cd ttc-delay-patterns-analysis
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Data
Place your TTC delay dataset in the `data/` folder as:

```text
data/ttc_delay_logs.csv
```

The project expects a CSV with fields similar to:
- date
- time
- route
- location
- delay_minutes
- incident_type

If your dataset uses different column names, the preprocessing script attempts to auto-detect common variants and normalize them.

## Run the Analysis
```bash
python main.py --input data/ttc_delay_logs.csv --output-dir results
```

This script will:
1. load and clean the dataset
2. engineer time-based features
3. summarize delay patterns
4. generate charts in the `results/` folder

## Example Insights
- weekday rush-hour delays are usually the most severe
- specific routes show consistent congestion patterns
- particular locations experience repeated delay clustering
- delay severity often rises during commuting periods and weather-affected conditions

## Skills Demonstrated
- data cleaning and preprocessing
- time-series feature engineering
- exploratory data analysis
- aggregation and trend analysis
- data visualization and dashboard-style reporting
- real-world transportation analytics

## License
This project is distributed under the MIT License.
