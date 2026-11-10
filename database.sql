-- ============================================================================
-- FILE DUMP DATABASE UAS PEMROGRAMAN WEB FRAMEWORK PYTHON
-- Bidang Studi Kasus : Bisnis (Prediksi Kebangkrutan Perusahaan)
-- Algoritma AI       : Multi-Layer Perceptron (MLPClassifier)
-- ============================================================================

CREATE DATABASE db_kebangkrutan;
USE db_kebangkrutan;

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

-- Data Awal (Sample Hasil Pemrosesan AI)
INSERT INTO riwayat_prediksi (
    nama_perusahaan, roa_c, net_income_to_assets, debt_ratio, net_worth_to_assets,
    current_ratio, quick_ratio, operating_gross_margin, cash_flow_to_assets,
    prediksi_label, status_prediksi, probabilitas_bangkrut
) VALUES
('PT Nusantara Sejahtera Tbk', 0.5420, 0.8350, 0.0850, 0.9150, 0.0165, 0.0112, 0.6180, 0.6590, 0, 'Perusahaan Sehat', 1.24),
('PT Global Tekstil Indotama', 0.3650, 0.6820, 0.2380, 0.7620, 0.0045, 0.0021, 0.5580, 0.5890, 1, 'Berisiko Bangkrut', 96.45),
('PT Prima Logistik Mandiri', 0.5180, 0.8190, 0.1020, 0.8980, 0.0148, 0.0098, 0.6090, 0.6480, 0, 'Perusahaan Sehat', 3.18),
('PT Krakatau Konstruksi Abadi', 0.3810, 0.7010, 0.2150, 0.7850, 0.0052, 0.0028, 0.5690, 0.5950, 1, 'Berisiko Bangkrut', 91.80);
