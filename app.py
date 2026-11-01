import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(
    page_title="NYC Crashes & Weather",
    layout="wide"
)

st.title("NYC Crashes & Weather")

st.write(
    "Explore NYC motor vehicle crashes in 2026 and examine how "
    "temperature, precipitation, and visibility relate to crash patterns."
)

st.write("**Audience:** NYC residents and transportation safety planners.")

# Load data
df = pd.read_csv("dashboard_crashes_2026.csv", low_memory=False)

df["crash_date"] = pd.to_datetime(df["crash_date"], errors="coerce")

numeric_columns = [
    "hour", "persons_injured", "persons_killed",
    "temperature_c", "precipitation_mm",
    "wind_speed_m_s", "visibility_km",
    "latitude", "longitude"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["borough"] = df["borough"].fillna("Unknown")

# Precipitation categories
df["precipitation_condition"] = "Not reported"

df.loc[
    df["precipitation_mm"] == 0,
    "precipitation_condition"
] = "No measurable precipitation"

trace = (
    df["precipitation_trace"]
    .fillna(False)
    .astype(str)
    .str.lower()
    .isin(["true", "1", "1.0"])
)

df.loc[
    trace & df["precipitation_mm"].isna(),
    "precipitation_condition"
] = "Trace precipitation"

df.loc[
    df["precipitation_mm"] > 0,
    "precipitation_condition"
] = "Measurable precipitation"


# DATE FILTERS
min_date = df["crash_date"].min().date()
max_date = df["crash_date"].max().date()

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start date",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

with col2:
    end_date = st.date_input(
        "End date",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

if start_date > end_date:
    st.error("Start date must be on or before end date.")
    st.stop()

# Filter by date
filtered_df = df[
    (df["crash_date"].dt.date >= start_date) &
    (df["crash_date"].dt.date <= end_date)
].copy()


# ADDITIONAL FILTERS
col1, col2 = st.columns(2)

with col1:
    borough_options = ["All"] + sorted(
        filtered_df["borough"].unique().tolist()
    )

    selected_borough = st.selectbox(
        "Borough",
        borough_options
    )

with col2:
    selected_road_user = st.selectbox(
        "Road user",
        ["All", "Pedestrians", "Cyclists", "Motorists"]
    )

if selected_borough != "All":
    filtered_df = filtered_df[
        filtered_df["borough"] == selected_borough
    ]

if selected_road_user == "Pedestrians":
    filtered_df = filtered_df[
        (filtered_df["pedestrians_injured"] > 0) |
        (filtered_df["pedestrians_killed"] > 0)
    ]

elif selected_road_user == "Cyclists":
    filtered_df = filtered_df[
        (filtered_df["cyclists_injured"] > 0) |
        (filtered_df["cyclists_killed"] > 0)
    ]

elif selected_road_user == "Motorists":
    filtered_df = filtered_df[
        (filtered_df["motorists_injured"] > 0) |
        (filtered_df["motorists_killed"] > 0)
    ]

if filtered_df.empty:
    st.warning("No crashes match these filters.")
    st.stop()


# SUMMARY METRICS
st.subheader("Crash Overview")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Crashes", f"{len(filtered_df):,}")

m2.metric(
    "Injury/Death Crashes",
    f"{filtered_df['injury_death_crash'].sum():,}"
)

m3.metric(
    "Fatal Crashes",
    f"{filtered_df['fatal_crash'].sum():,}"
)

m4.metric(
    "People Injured",
    f"{filtered_df['persons_injured'].fillna(0).sum():,.0f}"
)


# WEATHER VISUALIZATIONS
st.divider()
st.header("Weather and Crashes")


# CHART 1: PRECIPITATION
st.subheader("Crashes by Precipitation Condition")

precipitation_data = filtered_df[
    filtered_df["precipitation_condition"] != "Not reported"
]

if not precipitation_data.empty:

    precipitation_summary = (
        precipitation_data.groupby("precipitation_condition")
        .agg(
            Crashes=("collision_id", "count"),
            Injury_Death_Crashes=("injury_death_crash", "sum")
        )
    )

    fig, ax = plt.subplots(figsize=(6, 3))

    precipitation_summary.plot(kind="bar", ax=ax)

    ax.set_xlabel("Precipitation Condition", fontsize=10)
    ax.set_ylabel("Crash Records", fontsize=10)
    ax.set_title("Crashes by Precipitation", fontsize=12)
    ax.legend(["Total Crashes", "Injury/Death Crashes"], fontsize=9)
    ax.tick_params(axis="both", labelsize=9)

    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()

    st.pyplot(fig, width="content")
    plt.close(fig)

    highest = precipitation_summary["Crashes"].idxmax()

    st.caption(
        f"Among records with reported precipitation, "
        f"{highest} has the highest number of crashes."
    )

else:
    st.info("No reported precipitation observations in this selection.")

st.caption(
    "Missing precipitation measurements are not assumed to mean no rainfall."
)


# CHART 2: TEMPERATURE
st.subheader("Crashes Across Temperature Ranges")

temperature_data = filtered_df.dropna(
    subset=["temperature_c"]
).copy()

temperature_data["Temperature Range"] = pd.cut(
    temperature_data["temperature_c"],
    bins=[-30, -10, 0, 10, 20, 30, 40],
    labels=[
        "-30 to -10°C",
        "-10 to 0°C",
        "0 to 10°C",
        "10 to 20°C",
        "20 to 30°C",
        "Above 30°C"
    ]
)

temperature_summary = (
    temperature_data.groupby("Temperature Range", observed=False)
    .agg(
        Crashes=("collision_id", "count"),
        Injury_Death_Crashes=("injury_death_crash", "sum")
    )
)

fig, ax = plt.subplots(figsize=(6, 3))

temperature_summary.plot(kind="bar", ax=ax)

ax.set_xlabel("Temperature Range", fontsize=10)
ax.set_ylabel("Crash Records", fontsize=10)
ax.set_title("Crashes by Temperature", fontsize=12)
ax.legend(["Total Crashes", "Injury/Death Crashes"], fontsize=9)
ax.tick_params(axis="both", labelsize=9)

plt.xticks(rotation=20, ha="right")
plt.tight_layout()

st.pyplot(fig, width="content")
plt.close(fig)

if temperature_summary["Crashes"].sum() > 0:
    highest = temperature_summary["Crashes"].idxmax()
    st.caption(f"The highest crash count occurs in the {highest} range.")


# CHART 3: VISIBILITY
st.subheader("Crashes by Visibility")

visibility_data = filtered_df.dropna(
    subset=["visibility_km"]
).copy()

visibility_data["Visibility Range"] = pd.cut(
    visibility_data["visibility_km"],
    bins=[-0.01, 1, 5, 10, 20],
    labels=[
        "Under 1 km",
        "1–5 km",
        "5–10 km",
        "Above 10 km"
    ]
)

visibility_summary = (
    visibility_data.groupby("Visibility Range", observed=False)
    .size()
)

fig, ax = plt.subplots(figsize=(6, 3))

visibility_summary.plot(kind="bar", ax=ax)

ax.set_xlabel("Visibility Range", fontsize=10)
ax.set_ylabel("Crash Records", fontsize=10)
ax.set_title("Crashes by Visibility", fontsize=12)
ax.tick_params(axis="both", labelsize=9)

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig, width="content")
plt.close(fig)

if visibility_summary.sum() > 0:
    st.caption(
        f"Most crash records are in the "
        f"{visibility_summary.idxmax()} visibility range."
    )


# CRASH PATTERNS
st.divider()
st.header("Crash Patterns")


# CHART 4: HEATMAP
st.subheader("Crashes by Day and Hour")

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

heatmap = pd.crosstab(
    filtered_df["day_of_week"],
    filtered_df["hour"]
)

heatmap = heatmap.reindex(day_order)
heatmap = heatmap.reindex(columns=range(24), fill_value=0)

fig, ax = plt.subplots(figsize=(9, 3))

im = ax.imshow(
    heatmap,
    aspect="auto",
    cmap="YlOrRd"
)

ax.set_xlabel("Hour of Day (Eastern Time)", fontsize=10)
ax.set_ylabel("Day of Week", fontsize=10)
ax.set_title("Crash Records by Day and Hour", fontsize=12)

ax.set_xticks(range(24))

hour_labels = [
    f"{(hour - 1) % 12 + 1} {'AM' if hour < 12 else 'PM'}"
    for hour in range(24)
]

ax.set_xticklabels(
    hour_labels,
    rotation=45,
    ha="right",
    fontsize=8
)

ax.set_yticks(range(7))
ax.set_yticklabels(day_order, fontsize=9)

fig.colorbar(im, ax=ax, label="Crashes")

plt.tight_layout()

st.pyplot(fig, width="content")
plt.close(fig)

peak = heatmap.stack().idxmax()

peak_hour = peak[1]
peak_time = f"{(peak_hour - 1) % 12 + 1} {'AM' if peak_hour < 12 else 'PM'}"

st.caption(
    f"The busiest day-hour combination in this selection is "
    f"{peak[0]} at {peak_time}. Times use the recorded New York local clock."
)


# CHART 5: BOROUGH
st.subheader("Crashes by Borough")

borough_summary = (
    filtered_df.groupby("borough")
    .agg(
        Crashes=("collision_id", "count"),
        Injury_Death_Crashes=("injury_death_crash", "sum")
    )
)

fig, ax = plt.subplots(figsize=(6, 3))

borough_summary.plot(kind="bar", ax=ax)

ax.set_xlabel("Borough", fontsize=10)
ax.set_ylabel("Crash Records", fontsize=10)
ax.set_title("Crashes by Borough", fontsize=12)
ax.legend(["Total Crashes", "Injury/Death Crashes"], fontsize=9)
ax.tick_params(axis="both", labelsize=9)

plt.xticks(rotation=20, ha="right")
plt.tight_layout()

st.pyplot(fig, width="content")
plt.close(fig)

st.caption(
    f"{borough_summary['Crashes'].idxmax()} has the most crash records "
    "in the selected data."
)


# CHART 6: CONTRIBUTING FACTORS
st.subheader("Top Contributing Factors")

factors = (
    filtered_df[
        filtered_df["factor_1"].notna() &
        (filtered_df["factor_1"] != "Unspecified")
    ]["factor_1"]
    .value_counts()
    .head(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(7, 4))

factors.plot(kind="barh", ax=ax)

ax.set_xlabel("Crash Records", fontsize=10)
ax.set_ylabel("Contributing Factor", fontsize=10)
ax.set_title("Top 10 Vehicle 1 Contributing Factors", fontsize=12)
ax.tick_params(axis="both", labelsize=9)

plt.tight_layout()

st.pyplot(fig, width="content")
plt.close(fig)

if not factors.empty:
    st.caption(
        f"The most reported specified contributing factor is "
        f"{factors.idxmax()}."
    )


# MAP
st.divider()
st.subheader("NYC Crash Locations")

map_data = filtered_df[
    ["latitude", "longitude"]
].dropna().copy()

map_data = map_data[
    map_data["latitude"].between(40.45, 40.95) &
    map_data["longitude"].between(-74.30, -73.65)
]

map_data = map_data.rename(
    columns={
        "latitude": "lat",
        "longitude": "lon"
    }
)

if len(map_data) > 5000:
    map_data = map_data.sample(5000, random_state=42)

if not map_data.empty:

    st.map(
        map_data,
        latitude="lat",
        longitude="lon",
        zoom=10,
        size=25,
        height=450
    )

    st.caption(
        "Only coordinates within the NYC geographic bounds are displayed."
    )

else:
    st.info("No valid NYC coordinates are available for this selection.")


# DATA NOTES
st.divider()
st.subheader("Data Notes")

st.write(
    """
    - Crash data comes from NYC Open Data.
    - Weather observations come from NOAA's Central Park station.
    - Weather is matched using local crash date and hour.
    - One weather station may not represent conditions across every borough.
    - Crash counts show associations, not proof that weather caused crashes.
    - Missing precipitation observations are not treated as zero rainfall.
    """
)

st.caption("CIS 3400 | Project 1 | Fall 2026")