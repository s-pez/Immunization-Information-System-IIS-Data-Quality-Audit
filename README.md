# Immunization Information System (IIS) Data Quality Audit

A Python-based data quality assessment tool for immunization vaccination records. This project generates synthetic vaccination data with intentional data quality issues and provides comprehensive auditing capabilities to identify and flag data inconsistencies.

## Project Overview

This project consists of two main components:

1. **Data Generation** - Creates synthetic vaccination records with realistic and intentional data quality issues
2. **Data Quality Audit** - Analyzes vaccination data to identify completeness issues, invalid dates, duplicate patients, and dose sequence errors

## Files

### Scripts

- **Generate Data.py** - Generates synthetic vaccination dataset with 1,000 records including intentional duplicates and data quality issues
- **Audit Data Quality.py** - Performs comprehensive quality assessment on vaccination data

### Output Data Files

- **synthetic_vaccination_data.csv** - Generated synthetic vaccination records (1,000 records)
- **iis_data_with_quality_flags.csv** - Full dataset with quality flags appended
- **iis_quality_summary.csv** - Summary metrics of identified data quality issues
- **iis_duplicate_patients.csv** - List of patient records identified as duplicates

## Features

### Data Generation

The synthetic data generator creates:
- **1,000 vaccination records** with multiple vaccinations per patient
- **50 duplicate patient identities** with 6 records each
- **Realistic data** including:
  - Patient demographics (name, DOB, sex, zip code)
  - Vaccination details (vaccine type, dose number, administration date)
  - Provider information
- **Intentional data quality issues**:
  - Invalid administration dates (before date of birth)
  - Missing date of birth values (~3% of records)
  - Missing zip codes

### Data Quality Audit

The audit identifies:
- **Missing data** - Completeness analysis for all fields
- **Invalid dates** - Administration dates before date of birth
- **Duplicate patients** - Same name, last name, and DOB combinations
- **Dose sequence errors** - Incorrect dose progressions per vaccine type
- **Quality flags** - Records marked as "Valid" or "Issue"

## Usage

### Step 1: Generate Synthetic Data
```bash
python "Generate Data.py"
```
This creates `synthetic_vaccination_data.csv` with 1,000 vaccination records.

### Step 2: Run Data Quality Audit
```bash
python "Audit Data Quality.py"
```
This generates three output files:
- `iis_data_with_quality_flags.csv` - Original data plus quality assessment
- `iis_quality_summary.csv` - Summary metrics
- `iis_duplicate_patients.csv` - Duplicate patient details

## Data Dictionary

### Input Fields (synthetic_vaccination_data.csv)
| Field | Description | Data Type |
|-------|-------------|-----------|
| patient_id | Unique patient identifier | String |
| first_name | Patient first name | String |
| last_name | Patient last name | String |
| date_of_birth | Patient's date of birth | Date |
| sex | Patient gender (M/F) | String |
| zip_code | Patient's zip code | String |
| vaccine_type | Type of vaccine administered (MMR, DTaP, Polio, HepB, COVID-19) | String |
| dose_number | Dose sequence number (1, 2, or 3) | Integer |
| administration_date | Date vaccine was administered | Date |
| provider_id | Healthcare provider identifier | String |

### Output Fields (iis_data_with_quality_flags.csv)
All input fields plus:
| Field | Description | Data Type |
|-------|-------------|-----------|
| invalid_admin_date | Flag for administration date before DOB | Boolean |
| dose_sequence_error | Flag for incorrect dose sequence | Boolean |
| data_quality_flag | Overall quality assessment (Valid/Issue) | String |

## Quality Metrics

The audit generates summary metrics including:
- Total number of records
- Records with missing date of birth
- Invalid administration dates
- Dose sequence errors
- Number of duplicate patients

## Requirements

- Python 3.7+
- pandas
- numpy

## Installation

No installation required. Simply ensure pandas and numpy are installed:

```bash
pip install pandas numpy
```

## Author

Sarita Perez

## License

MIT License
