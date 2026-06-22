import psycopg2

import pandas as pd
import json
from datetime import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="assignment1",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# Load tables into pandas

tables = {}
for tbl in ["sex_birth", "staff_dept", "tel_email"]:
    tables[tbl] = pd.read_sql(f"SELECT * FROM {tbl};", conn)


# Cleaning functions

def clean_sex(val):
    return val if val in ["M", "F"] else None

def clean_date(val):
    try:
        return pd.to_datetime(val, errors="coerce")
    except:
        return None

def clean_email(val):
    return val if "@" in str(val) else None

def clean_phone(val):
    return val if len(str(val)) >= 8 else None


# Apply cleaning

tables["sex_birth"]["sex"] = tables["sex_birth"]
["sex"].apply(clean_sex)

tables["sex_birth"]["birthday"] = tables["sex_birth"]
["birthday"].apply(clean_date)

tables["tel_email"]["email_address"] = tables["tel_email"]
["email_address"].apply(clean_email)

tables["tel_email"]["telephone_no"] = tables["tel_email"]
["telephone_no"].apply(clean_phone)


# Drop invalid rows

for key in tables:
    tables[key].dropna(inplace=True)


# Remove duplicates

for key in tables:
    tables[key].drop_duplicates(subset=["name"],inplace=True)


# Export cleaned data back

for key, df in tables.items():
    df.to_sql(key + "_cleaned", conn, if_exists="replace", index=False)


# Save JSON for API use

with open("cleaned_data.json", "w") as f:
    json.dump({k: v.to_dict(orient="records") for k, v in tables.items()}, f, indent=4)


print("Data cleaned and exported successfully!")