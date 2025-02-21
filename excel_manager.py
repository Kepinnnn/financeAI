import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from model import classify_expense

# Setup autentikasi untuk Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credential.json", scopes=scope)
client = gspread.authorize(creds)

# Buka Google Sheet (ganti "Finance Data" dengan nama sheet kamu)
sheet = client.open("FINANCE DATA").sheet1

def save_to_google_sheet(amount, description, payment):
    # Menentukan kategori pengeluaran dengan memanggil fungsi classify_expense
    category = classify_expense(description)
    # Mendapatkan nama bulan saat ini (contoh: "February")
    month = datetime.now().strftime("%B")
    day = datetime.now().strftime("%D")

    
    sheet.append_row(["Tanggal", "Bulan", "Jumlah", "Deskripsi", "Kategori", "Payment"])

    # Data baru yang akan disimpan (sesuai header: Bulan, Jumlah, Deskripsi, Kategori)
    new_row = [day, month, amount, description, category, payment]
    # Menambahkan data ke Google Sheet
    sheet.append_row(new_row)
    
    # Mengambil semua record dari Google Sheet
    records = sheet.get_all_records()

    # Menghitung total pengeluaran untuk bulan ini dari kolom "Jumlah"
    monthly_total = sum(float(rec["Jumlah"]) for rec in records if rec["Bulan"] == month)
    daily_total = sum(float(rec["Jumlah"]) for rec in records if rec["Tanggal"] == day)
    return monthly_total, daily_total
    