import streamlit as st
import gspread
import pandas as pd
import time
from google.oauth2.service_account import Credentials
from google_sheet_manager import save_to_google_sheet

# Setup Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Buka Google Sheet, ganti 'Finance Data' dengan nama sheet kamu
sheet = client.open("FINANCE DATA").sheet1

st.title("AI Pencatat Pengeluaran")

header = st.image("header.png")
amount = st.number_input("Masukkan jumlah pengeluaran:")
description = st.text_input("Deskripsi pengeluaran:")
options = ["QRIS", "Cash"]
payment = st.segmented_control(
    "Bayar pake apa ?", options, selection_mode="single"
)
st.markdown(f"Your selected options: {payment}.")

if st.button("Simpan"):
    with st.spinner("Wait for it...", show_time=True):
        time.sleep(3)
    
    monthly_total,daily_total, sentiment_results  = save_to_google_sheet(amount, description, payment)
    st.success("Pengeluaran berhasil disimpan!")
    
    st.write(f"Total pengeluaran bulan ini: {monthly_total}")

    # Tampilkan hasil analisis sentimen
    st.write("🔍 **Analisis Sentimen Pengeluaran:**")
    st.write(f"✅ Positif: {sentiment_results['positive']}")
    st.write(f"🟡 Netral: {sentiment_results['neutral']}")
    st.write(f"❌ Negatif: {sentiment_results['negative']}")
    
    if monthly_total > 2000000:
        st.error("Sudah mencapai batasan bulan ini bro !")

    if daily_total > 100000:
        st.error("Hari ini udah limit bro !!")

if st.button("Reset Data Google Sheets"):
    # Reset: Hapus semua data di sheet, lalu tambahkan ulang header
    sheet = None  # kita dapatkan objek sheet lagi
    # Untuk menghindari masalah, ambil objek sheet dari client
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    from google.oauth2.service_account import Credentials
    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("Finance Data").sheet1

    sheet.clear()
    # Tambahkan header yang diinginkan; misalnya: Bulan, Jumlah, Deskripsi, Kategori
    sheet.append_row(["Day", "Bulan", "Jumlah", "Deskripsi", "Kategori", "Payment"])
    st.success("Semua data di Google Sheets telah di-reset yaa!")
