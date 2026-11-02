# NYC Motor Vehicle Crashes & Weather Analysis

## Project Overview
This project analyzes motor vehicle crashes in New York City using NYC Open Data and hourly weather data from NOAA. It explores crash patterns by time, location, contributing factors, and weather conditions.

## Live Dashboard
[View the NYC Crashes & Weather Dashboard](https://nyccrashanalysis.streamlit.app/)

## Research Questions
- How do crashes vary by day and time?
- Which boroughs have the most crashes?
- What are the most common contributing factors?
- How do crash counts vary across weather conditions?
- Where are crashes geographically concentrated?
- How many crashes involve injuries or fatalities?

## Data Sources
- **NYC Open Data:** [Motor Vehicle Collisions – Crashes](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)
- **NOAA:** Hourly weather observations from Central Park, NYC.

## Technologies
Python, Pandas, Matplotlib, Streamlit, and Jupyter Notebook.

## Repository Structure
```text
NYCCrashAnalysis/
├── app.py
├── dashboard_crashes_2026.csv
├── noaa_nyc_hourly_weather_2026.ipynb
├── NYC_Crashes_Analysis_With_Weather_Data_Merge.ipynb
├── README.md
└── requirements.txt
```

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Weather data comes from one station in Central Park and may not represent all boroughs. The analysis shows associations, not causation. Crash counts also do not account for traffic volume.

## AI Statement
AI tools were used to assist in generating and debugging code for the Streamlit dashboard. The data analysis, project decisions, and final review were completed by the author.