# Week 3 - Python & Data Wrangling
# Skill Nexis Data Analyst Course

import pandas as pd

df = pd.read_csv("data.csv")

# Clean date values
df["Date"] = df["Date"].astype("string").str.strip().str.strip("'").str.strip('"')
df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d", errors="coerce")
mask = df["Date"].isna() & df["Date"].notna()
# Handle YYYYMMDD values separately
raw_dates = pd.read_csv("data.csv")["Date"]
df.loc[df["Date"].isna() & raw_dates.notna(), "Date"] = pd.to_datetime(
    raw_dates[df["Date"].isna() & raw_dates.notna()].astype(str).str.replace(r"\.0$", "", regex=True),
    format="%Y%m%d", errors="coerce"
)

# Fill the missing date from the chronological sequence
df.loc[df["Date"].isna(), "Date"] = pd.Timestamp("2020-12-22")

# Fill missing Calories with the median
df["Calories"] = df["Calories"].fillna(df["Calories"].median())

# Remove duplicate rows
df = df.drop_duplicates()

# Filter rows: keep realistic workout durations of 120 minutes or less
df = df[df["Duration"] <= 120].copy()

# Create new columns
df["Calories_per_Minute"] = (df["Calories"] / df["Duration"]).round(2)
df["Pulse_Range"] = df["Maxpulse"] - df["Pulse"]

print(df.info())
print(df.head())
print(df.describe())
print(df.to_string(index=False))
