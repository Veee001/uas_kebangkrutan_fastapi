========================================================================
PANDUAN MENJALANKAN PROJECT UAS PEMROGRAMAN WEB FRAMEWORK PYTHON
Judul   : Sistem Prediksi Kebangkrutan Perusahaan (MLP Neural Network)
Pembuat : Saverio Ferlando
========================================================================

Project ini SUDAH DILENGKAPI dengan:
1. File model AI yang sudah dilatih ('model_mlp.pkl' & 'scaler.pkl')
2. Dataset 'data.csv' & script pelatihan 'train_model.py'
3. File database 'database.sql'
4. Auto-Installer Database di 'main.py' (otomatis membuat database & tabel saat dijalankan!)

CARA MENJALANKAN (LANGSUNG BISA DIGUNAKAN):
------------------------------------------------------------------------
Langkah 1: Nyalakan MySQL di XAMPP atau Laragon.
           (Catatan: Secara default menggunakan user="root" dan password="".
            Jika MySQL kamu memakai password, ubah bagian DB_CONFIG di main.py).

Langkah 2: Buka Terminal / CMD di dalam folder ini, lalu install library:
           pip install -r requirements.txt

Langkah 3: (Opsional) Jika ingin melatih ulang model dari awal:
           python train_model.py

Langkah 4: Jalankan server FastAPI:
           uvicorn main:app --reload

Langkah 5: Buka browser dan akses:
           http://127.0.0.1:8000
========================================================================
