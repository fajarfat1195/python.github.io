import os
from typing import Dict, Any, Tuple
from google.cloud import bigquery
import pandas as pd

# --- KONFIGURASI ---
PROJECT_ID = "celtic-fact-367202"
DATASET_ID = "test"
SOURCE_TABLE = "pokemon"
DESTINATION_TABLE = "pokemon"

# --- FUNGSI DASAR ---

def get_client() -> bigquery.Client | None:
    """Inisialisasi BigQuery client."""
    try:
        client = bigquery.Client()
        print("✅ BigQuery client initialized.")
        return client
    except Exception as e:
        print(f"❌ Error initializing BigQuery client: {e}")
        return None

def fetch_table(client: bigquery.Client, table: str) -> pd.DataFrame:
    """Ambil data (maks 100 baris) dari tabel BigQuery."""
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{table}` LIMIT 100"
    try:
        df = client.query(query).to_dataframe()
        print(f"✅ Fetched {len(df)} rows from {table}.")
        return df
    except Exception as e:
        print(f"❌ Fetch error: {e}")
        return pd.DataFrame()

def mock_data() -> pd.DataFrame:
    """Buat data dummy untuk uji upload."""
    print("🧪 Generating mock data...")
    data = [
        {"#": 1001, "Name": "Pikachu Prime", "Type_1": "Electric", "Type_2": None, "HP": 150, "Attack": 120, "Defense": 90, "Sp_Atk": 150, "Sp_Def": 90, "Speed": 180, "Generation": 10, "Legendary": True},
        {"#": 1002, "Name": "Bulbasaur Beta", "Type_1": "Grass", "Type_2": "Poison", "HP": 100, "Attack": 70, "Defense": 70, "Sp_Atk": 80, "Sp_Def": 100, "Speed": 60, "Generation": 10, "Legendary": False},
    ]
    return pd.DataFrame(data)

def append_data(client: bigquery.Client, df: pd.DataFrame, table: str) -> int:
    """Append data ke tabel BigQuery."""
    if df.empty:
        print("⚠️ DataFrame kosong, tidak ada data untuk ditulis.")
        return 0

    table_path = f"{PROJECT_ID}.{DATASET_ID}.{table}"
    config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")

    try:
        job = client.load_table_from_dataframe(df, table_path, job_config=config)
        job.result()
        print(f"✅ {job.output_rows} rows appended to {table_path}.")
        return job.output_rows
    except Exception as e:
        print(f"❌ Append error: {e}")
        return 0

# --- FUNGSI UNTUK FLASK ROUTES ---

def fetch_data_only() -> Tuple[Dict[str, Any], int]:
    """Endpoint /fetch-data → Ambil data BigQuery."""
    client = get_client()
    if not client:
        return {"status": "ERROR", "message": "Cannot initialize BigQuery client."}, 500

    df = fetch_table(client, SOURCE_TABLE)
    if df.empty:
        return {"status": "ERROR", "message": f"No data found in {SOURCE_TABLE}."}, 404

    return {
        "status": "SUCCESS",
        "message": f"Fetched {len(df)} rows from {SOURCE_TABLE}.",
        "data_preview": df.to_dict("records")
    }, 200

def run_bigquery_pipeline() -> Tuple[Dict[str, Any], int]:
    """Endpoint /run-bigquery → Tambah data dummy ke tabel BigQuery."""
    client = get_client()
    if not client:
        return {"status": "ERROR", "message": "Cannot initialize BigQuery client."}, 500

    df_new = mock_data()
    rows = append_data(client, df_new, DESTINATION_TABLE)

    if rows > 0:
        return {"status": "SUCCESS", "message": f"{rows} rows appended to {DESTINATION_TABLE}."}, 200
    else:
        return {"status": "ERROR", "message": "Failed to append data."}, 500

# --- DEBUG LOKAL ---
if __name__ == "__main__":
    print("🚀 Testing BigQuery pipeline locally...")
    client = get_client()
    if client:
        print(fetch_data_only())
        print(run_bigquery_pipeline())
