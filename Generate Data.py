import pandas as pd
import numpy as np
from datetime import timedelta
import random

# Set random seed for reproducibility
random.seed(42)

n_records = 1000

# Define possible values for each field
first_names = ["John", "Jane", "Maria", "Luis", "Aisha", "Michael", "Sarah"]
last_names = ["Smith", "Johnson", "Garcia", "Brown", "Lopez", "Williams"]
vaccines = ["MMR", "DTaP", "Polio", "HepB", "COVID-19"]
providers = ["Clinic_A", "Clinic_B", "Hospital_C"]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


# Create intentional duplicate people

n_duplicate_people = 50      # number of true duplicate identities
records_per_duplicate = 6    # how many times each appears

duplicate_people = []

for i in range(n_duplicate_people):
    duplicate_people.append({
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "date_of_birth": random_date(
            pd.Timestamp("2015-01-01"),
            pd.Timestamp("2022-01-01")
        )
    })

data = []

# -----------------------------
# Generate duplicate records
# -----------------------------
for person in duplicate_people:
    for _ in range(records_per_duplicate):
        admin_date = random_date(
            pd.Timestamp("2016-01-01"),
            pd.Timestamp("2025-01-01")
        )

        # introduce some invalid admin dates
        if random.random() < 0.05:
            admin_date = person["date_of_birth"] - timedelta(days=random.randint(1, 100))

        data.append({
            "patient_id": f"P{random.randint(1, 500)}",
            "first_name": person["first_name"],
            "last_name": person["last_name"],
            "date_of_birth": person["date_of_birth"],  # NEVER NULL
            "sex": random.choice(["M", "F"]),
            "zip_code": random.choice(["21201", "21202", "21203", None]),
            "vaccine_type": random.choice(vaccines),
            "dose_number": random.choice([1, 2, 3]),
            "administration_date": admin_date,
            "provider_id": random.choice(providers)
        })


# Generate remaining random (mostly unique) records
while len(data) < n_records:
    dob = random_date(pd.Timestamp("2015-01-01"), pd.Timestamp("2022-01-01"))

    data.append({
        "patient_id": f"P{random.randint(1, 500)}",
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "date_of_birth": dob if random.random() > 0.03 else pd.NaT,
        "sex": random.choice(["M", "F"]),
        "zip_code": random.choice(["21201", "21202", "21203", None]),
        "vaccine_type": random.choice(vaccines),
        "dose_number": random.choice([1, 2, 3]),
        "administration_date": random_date(
            pd.Timestamp("2016-01-01"),
            pd.Timestamp("2025-01-01")
        ),
        "provider_id": random.choice(providers)
    })

df = pd.DataFrame(data)

df.to_csv("synthetic_vaccination_data.csv", index=False)
print("Synthetic vaccination data generated with intentional dup_key duplicates.")
