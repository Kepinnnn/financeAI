import pandas as pd
from datetime import datetime
from model import classify_expense

def save_to_excel(amount, description, payment):
    category = classify_expense(description)
    month = datetime.now().strftime("%B")
    day = datetime.now().strftime("%D")
    
    # Coba buka file Excel yang sudah ada, kalau belum ada buat DataFrame baru
    try:
        df = pd.read_excel("data/transactions.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Tanggal", "Bulan", "Jumlah", "Deskripsi", "Pembayaran", "Kategori"])
    
    new_data = pd.DataFrame({
        'Tanggal': [day],
        "Bulan": [month],
        "Jumlah": [amount],
        "Deskripsi": [description],
        "Pembayaran": [payment],
        "Kategori": [category]
    })
    
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel("data/transactions.xlsx", index=False)

    monthly_total = df[df["Bulan"] == month]["Jumlah"].sum()
    return monthly_total