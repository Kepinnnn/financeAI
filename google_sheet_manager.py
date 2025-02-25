import gspread
import os
import json
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

# Ambil credential dari environment variable (GitHub Secrets / Streamlit Secrets)
credentials_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

# Fix format private key
credentials_json["private_key"] = credentials_json["private_key"].replace("\\n", "\n")

creds = Credentials.from_service_account_info(credentials_json)
client = gspread.authorize(creds)

SHEET_NAME = "FINANCE DATA"
sheet = client.open(SHEET_NAME).sheet1

def save_to_google_sheet(amount, description, payment):

    from model import classify_expense
    from model import analyze_spending_trend

    # Menentukan kategori pengeluaran dengan memanggil fungsi classify_expense
    category = classify_expense(description)
    # Mendapatkan nama bulan saat ini (contoh: "February")
    month = datetime.now().strftime("%B")
    day = datetime.now().strftime("%D")

    # Cek apakah header sudah ada dengan mengambil baris pertama
    first_row = sheet.row_values(1)

    # Kalau baris pertama kosong atau bukan header yang kita harapkan, tambahkan header
    expected_header = ["Tanggal", "Bulan", "Jumlah", "Deskripsi", "Kategori", "Payment"]
    if not first_row or first_row != expected_header:
        sheet.insert_row(expected_header, 1)  # Tambahkan header di baris pertama

    sentiment_results = analyze_spending_trend([description])

    # Data baru yang akan disimpan (sesuai header: Bulan, Jumlah, Deskripsi, Kategori)
    new_row = [day, month, amount, description, category, payment]
    # Menambahkan data ke Google Sheet
    sheet.append_row(new_row)
    
    # Mengambil semua record dari Google Sheet
    records = sheet.get_all_records()

    # Menghitung total pengeluaran untuk bulan ini dari kolom "Jumlah"
    monthly_total = sum(float(rec["Jumlah"]) for rec in records if rec["Bulan"] == month)
    daily_total = sum(float(rec["Jumlah"]) for rec in records if rec["Tanggal"] == day)
    return monthly_total, daily_total, sentiment_results
    
