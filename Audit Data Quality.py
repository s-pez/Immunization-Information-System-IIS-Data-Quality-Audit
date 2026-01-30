import pandas as pd
import numpy as np
from datetime import timedelta

# Load the synthetic vaccination data
df = pd.read_csv("synthetic_vaccination_data.csv", parse_dates=["date_of_birth", "administration_date"])

# Audit for data completeness and validity
completeness = df.isnull().mean().reset_index()
completeness.columns = ["field", "missing_rate"]
df["invalid_admin_date"] = df["administration_date"] < df["date_of_birth"]

# Identify duplicate records based on patient_id and vaccine_type
dose_errors = (
    df.sort_values("administration_date")
      .groupby(["patient_id", "vaccine_type"])["dose_number"]
      .apply(lambda x: (x.diff() < 0).any())
      .reset_index(name="dose_sequence_error")
)

# Create a duplicate key for more robust duplicate detection
df["dup_key"] = (
    df["first_name"].str.lower() + "_" +
    df["last_name"].str.lower() + "_" +
    df["date_of_birth"].astype(str)
)

duplicate_summary = (
        df.groupby(["first_name", "last_name", "date_of_birth"]) 
            .size()
            .reset_index(name="record_count")
            .query("record_count > 1")
)

# Merge dose sequence errors back to the main DataFrame
df = df.merge(dose_errors, on=["patient_id", "vaccine_type"], how="left")

df["dose_sequence_error"] = df["dose_sequence_error"].fillna(False)

# Flag records with any data quality issues
df["data_quality_flag"] = np.where(
    (df["invalid_admin_date"]) |
    (df["dose_sequence_error"]) |
    (df["date_of_birth"].isnull()),
    "Issue",
    "Valid"
)

# Summary of data quality issues
data_quality_summary = df["data_quality_flag"].value_counts().reset_index()
data_quality_summary.columns = ["data_quality_flag", "count"]

# Generate summary metrics
summary_metrics = pd.DataFrame({
    "metric": [
        "Total Records",
        "Records with Missing DOB",
        "Invalid Administration Dates",
        "Dose Sequence Errors",
        "Duplicate Patients"
    ],
    "value": [
        len(df),
        df["date_of_birth"].isnull().sum(),
        df["invalid_admin_date"].sum(),
        df["dose_sequence_error"].sum(),
        duplicate_summary.shape[0]
    ]
})

# Save results
df.to_csv("iis_data_with_quality_flags.csv", index=False)
summary_metrics.to_csv("iis_quality_summary.csv", index=False)
duplicate_summary.to_csv("iis_duplicate_patients.csv", index=False)
print("Data quality audit completed. Results saved to 'iis_data_with_quality_flags.csv', 'iis_quality_summary.csv', and 'iis_duplicate_patients.csv'.")