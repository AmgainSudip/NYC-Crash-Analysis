# NYC Motor Vehicle Crashes & Weather Analysis

## Project Overview
This project analyzes New York City motor vehicle crashes using crash records from NYC Open Data and hourly weather observations from NOAA. It explores patterns in crash frequency, location, contributing factors, injuries, fatalities, and weather conditions.

## Intended Audience
This project is intended for students, researchers, transportation professionals, and anyone interested in traffic safety and urban data analysis. The dashboard allows users to explore NYC crash patterns and examine how they vary across time, locations, and weather conditions.

## Live Dashboard
[View the NYC Crashes & Weather Dashboard](https://nyccrashanalysis.streamlit.app/)

## Dataset Sources
- **NYC Open Data:** [Motor Vehicle Collisions – Crashes](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95) – Provides crash dates, times, boroughs, contributing factors, and injury and fatality records.
- **NOAA:** Hourly weather observations from Central Park, NYC – Provides temperature, precipitation, wind speed, and visibility data.

The two datasets were combined using the crash date and hour.

## Analysis Questions
- How do crashes vary by day and time?
- Which boroughs have the highest number of crashes?
- What are the most common contributing factors?
- How do crash counts vary across different weather conditions?
- Where are crashes geographically concentrated?
- How many crashes involve injuries or fatalities?

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