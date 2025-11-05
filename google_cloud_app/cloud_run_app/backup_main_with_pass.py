import os
from flask import Flask, jsonify, request
from utils import calculate_time_based_message
from bigquery_pipeline import fetch_data_only, run_bigquery_pipeline

# AUTH_TOKEN di define ulang disini, supaya ketika menjalankannya di lokal. AUTH_TOKEN tetap dikenali
# Value variable ini juga di taruh di variable and secrets
# Jadi jika ingin digunakan di project sungguhan dan running di cloud, cukup get "AUTH TOKEN" saja. Jangan define valuenya lagi
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "fajarfatoni123456")  # Static password

# --- Inisialisasi Aplikasi Flask ---
app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8080))

# --- Fungsi Bantuan ---
def footer(author="Gemini"):
    return f"\n\n--- Dibuat oleh {author} untuk Cloud Run ---"

def require_auth(func):
    """Decorator untuk proteksi endpoint dengan static token."""
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-API-KEY")
        if token != AUTH_TOKEN:
            return jsonify({"status": "ERROR", "message": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# --- ROUTES ---

@app.route("/", methods=["GET", "POST"])
@require_auth
def home():
    """Endpoint utama untuk pengecekan deploy."""
    message = f"{calculate_time_based_message()}. Aplikasi Cloud Run Anda berhasil di-deploy."
    return message + footer()

@app.route("/fetch-data", methods=["GET", "POST"])
@require_auth
def fetch_data():
    """Menampilkan preview data dari BigQuery."""
    data, status = fetch_data_only()
    data["footer"] = footer()
    return jsonify(data), status

@app.route("/run-bigquery", methods=["GET", "POST"])
@require_auth
def run_pipeline():
    """Menjalankan pipeline ETL BigQuery."""
    data, status = run_bigquery_pipeline()
    data["footer"] = footer()
    return jsonify(data), status

# --- Mode Lokal ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)

