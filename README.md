# Time-Series Analysis: TTC Delay Patterns

A polished Python project for exploring Toronto Transit Commission (TTC) delay trends and congestion behavior through data cleaning, time-series analysis, and visualization.

## Project Overview
This project analyzes a synthetic TTC delay dataset containing more than 100,000 records to uncover temporal and spatial congestion patterns. By cleaning inconsistent fields, normalizing timestamps, and aggregating delays across routes and stations, the analysis highlights when and where service disruptions are most frequent.

The work is designed to demonstrate:
- data wrangling with Pandas
- time-series feature engineering
- transit delay analysis
- exploratory data analysis (EDA)
- visual storytelling with Matplotlib and Seaborn

## Why This Project Matters
Urban mobility systems are highly sensitive to delays, crowding, and service interruptions. TTC delay data can reveal recurring patterns such as:
- morning and evening rush-hour congestion spikes
- route-specific service instability
- recurring hotspots around frequent transit nodes
- systematic service disruptions tied to time-of-day and weekday patterns

This project turns raw operational data into actionable insight for transit service analysis and planning.

## Skills Demonstrated
- Python data analytics
- Pandas preprocessing and aggregation
- Time-series feature engineering
- Missing-value handling and data cleansing
- Route and location-level analysis
- Matplotlib/Seaborn data visualization
- Real-world transportation analytics

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Repository Structure
```text
.
├── data/
│   ├── generate_ttc_dataset.py
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
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
└── .python-version
```

## Data Generation
The project includes a synthetic dataset generator so it runs immediately without external data:

```bash
python data/generate_ttc_dataset.py
```

This creates a realistic TTC-style CSV at:

```text
data/ttc_delay_logs.csv
```

## Running the Analysis
1. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Generate or place the dataset:

```bash
python data/generate_ttc_dataset.py
```

3. Run the analysis pipeline:

```bash
python main.py --input data/ttc_delay_logs.csv --output-dir results
```

## Output
The pipeline produces summary statistics and stores visualizations in the `results/` folder, including:
- average delay by hour of day
- average delay by day of week
- top routes by delay severity
- top locations by delay frequency and severity

## Example Insights
- Peak delay concentrations appear during commuting windows
- Certain routes consistently show higher delay severity
- Delay frequency is concentrated in busy terminal and corridor locations
- Transit disruptions display strong temporal structure, which is valuable for operational planning

## Project Goal Statement
This project was built to answer a practical question: when and where do TTC delays cluster most heavily, and what patterns can be extracted from noisy operational data? The answer is delivered through systematic preprocessing, aggregation, and visual analysis.

## License
This project is available under the MIT License.
