import polars as pl
import os
from dotenv import load_dotenv

load_dotenv()

storage_options = {
    "account_name": "civicpulse22456",
    "account_key": os.getenv('ACCOUNT_KEY'), 
}

def transform():
    print("ACCOUNT_KEY:", os.getenv("ACCOUNT_KEY"))

    source_uri = "az://bronze/civic_logic_requests.csv"
    target_uri = "az://silver/civic_logic_requests.parquet"

    df = pl.scan_csv(source_uri, storage_options=storage_options)

    column_mapping = {
        "created_date": "created_date",
        "closed_date": "closed_date",
        "complaint_type": "problem",
        "descriptor": "problem_detail",
        "location_type": "location_type",
        "incident_address": "incident_address",
        "city": "city",
        "borough": "borough",
        "latitude": "latitude",
        "longitude": "longitude"
    }

    # Select and rename
    df_refined = df.select([
        pl.col(old).alias(new) for old, new in column_mapping.items()
    ])

    # Save to Silver layer
    df_refined.sink_parquet(
        target_uri,
        storage_options=storage_options,
        compression="snappy"
    )

    print(f"data loaded to {target_uri}")