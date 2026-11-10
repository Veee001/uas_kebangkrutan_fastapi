# File: main.py
import json
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2
from psycopg2.extras import RealDictCursor
import joblib
import numpy as np

app = FastAPI(title="FinRisk AI - Sistem Prediksi Kebangkrutan Perusahaan (MLP)")

# Mount folder static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load Model AI & Scaler
MODEL_PATH = "model_mlp.pkl"
SCALER_PATH = "scaler.pkl"
METRICS_PATH = "metrics.json"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return {
        "accuracy": 96.67, "precision": 93.18, "recall": 85.42, "f1_score": 89.13,
        "confusion_matrix": [[249, 3], [7, 41]], "total_data": 1500, "train_size": 1200, "test_size": 300, "n_iterations": 300
    }

# --- KONFIGURASI KONEKSI POSTGRESQL (pgAdmin 4) ---
DB_CONFIG = {
    "host": "localhost",
    "database": "db_kebangkrutan",
    "user": "postgres",           # Username default pgAdmin 4
    "password": "061112"                # Masukkan password pgAdmin Anda di sini jika ada
}

def init_database():
    """Inisialisasi tabel riwayat_prediksi secara otomatis di PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS riwayat_prediksi (
                id SERIAL PRIMARY KEY,
                nama_perusahaan VARCHAR(150) NOT NULL,
                roa_c DOUBLE PRECISION NOT NULL,
                net_income_to_assets DOUBLE PRECISION NOT NULL,
                debt_ratio DOUBLE PRECISION NOT NULL,
                net_worth_to_assets DOUBLE PRECISION NOT NULL,
                current_ratio DOUBLE PRECISION NOT NULL,
                quick_ratio DOUBLE PRECISION NOT NULL,
                operating_gross_margin DOUBLE PRECISION NOT NULL,
                cash_flow_to_assets DOUBLE PRECISION NOT NULL,
                prediksi_label INT NOT NULL,
                status_prediksi VARCHAR(50) NOT NULL,
                probabilitas_bangkrut DOUBLE PRECISION NOT NULL,
                waktu_input TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.close()
        conn.close()
        print("[INFO] Koneksi & Tabel PostgreSQL (pgAdmin 4) berhasil disiapkan!")
    except Exception as e:
        print(f"[PERINGATAN KONEKSI PG] Gagal terhubung ke pgAdmin 4: {e}")

# Jalankan inisialisasi database saat startup
init_database()

def get_db_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        cursor_factory=RealDictCursor
    )

# 1. Untuk Halaman Home
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    metrics = load_metrics()
    return templates.TemplateResponse(request, "home.html", {"metrics": metrics})

# 2. Untuk Halaman Contact Us
@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return templates.TemplateResponse(request, "contact.html")

# 3. Untuk Halaman Prediksi
@app.get("/predict", response_class=HTMLResponse)
async def predict_page(request: Request):
    riwayat = []
    db_error = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM riwayat_prediksi ORDER BY id DESC")
            riwayat = cursor.fetchall()
        conn.close()
    except Exception as e:
        db_error = f"Gagal terhubung ke database: {e}"
    
    return templates.TemplateResponse(
        request, "predict.html", {"riwayat": riwayat, "db_error": db_error}
    )

# 4. OPERASI CREATE: PREDIKSI MODEL AI & SIMPAN KE POSTGRESQL (Soal 3a)
@app.post("/predict")
async def create_prediction(
    nama_perusahaan: str = Form(...),
    roa_c: float = Form(...),
    net_income_to_assets: float = Form(...),
    debt_ratio: float = Form(...),
    net_worth_to_assets: float = Form(...),
    current_ratio: float = Form(...),
    quick_ratio: float = Form(...),
    operating_gross_margin: float = Form(...),
    cash_flow_to_assets: float = Form(...)
):
    input_features = np.array([[
        roa_c, net_income_to_assets, debt_ratio, net_worth_to_assets,
        current_ratio, quick_ratio, operating_gross_margin, cash_flow_to_assets
    ]])

    input_scaled = scaler.transform(input_features)
    pred_label = int(model.predict(input_scaled)[0])
    pred_proba = float(model.predict_proba(input_scaled)[0][1]) * 100

    status_teks = "Berisiko Bangkrut" if pred_label == 1 else "Perusahaan Sehat"

    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = """
            INSERT INTO riwayat_prediksi 
            (nama_perusahaan, roa_c, net_income_to_assets, debt_ratio, net_worth_to_assets, 
             current_ratio, quick_ratio, operating_gross_margin, cash_flow_to_assets, 
             prediksi_label, status_prediksi, probabilitas_bangkrut)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            nama_perusahaan, roa_c, net_income_to_assets, debt_ratio, net_worth_to_assets,
            current_ratio, quick_ratio, operating_gross_margin, cash_flow_to_assets,
            pred_label, status_teks, round(pred_proba, 2)
        ))
    conn.commit()
    conn.close()

    return RedirectResponse(url="/predict", status_code=303)

# 5. OPERASI DELETE: HAPUS DATA DARI POSTGRESQL (Soal 3c)
@app.post("/delete/{item_id}")
async def delete_prediction(item_id: int):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM riwayat_prediksi WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/predict", status_code=303)