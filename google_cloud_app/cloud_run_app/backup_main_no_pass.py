import os
from flask import Flask, jsonify, request
from utils import calculate_time_based_message
from bigquery_pipeline import fetch_data_only, run_bigquery_pipeline

# --- Inisialisasi Aplikasi Flask ---
app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8080))

# --- Fungsi Bantuan ---
def footer(author="Gemini"):
    return f"\n\n--- Dibuat oleh {author} untuk Cloud Run ---"

# --- ROUTES ---

@app.route("/", methods=["GET", "POST"])
def home():
    """Endpoint utama untuk pengecekan deploy."""
    message = f"{calculate_time_based_message()}. Aplikasi Cloud Run Anda berhasil di-deploy."
    return message + footer()

@app.route("/fetch-data", methods=["GET", "POST"])
def fetch_data():
    """Menampilkan preview data dari BigQuery."""
    data, status = fetch_data_only()
    data["footer"] = footer()
    return jsonify(data), status

@app.route("/run-bigquery", methods=["GET", "POST"])
def run_pipeline():
    """Menjalankan pipeline ETL BigQuery."""
    data, status = run_bigquery_pipeline()
    data["footer"] = footer()
    return jsonify(data), status

# --- Mode Lokal ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)



