import streamlit as st
from excel_manager import save_to_excel
import time

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
        time.sleep(5)

    monthly_total = save_to_excel(amount, description, payment)
    st.success("Pengeluaran berhasil disimpan!")
    
    # Menampilkan total pengeluaran untuk bulan ini
    st.write(f"Total pengeluaran bulan ini: {monthly_total}")
    
    # Cek jika total pengeluaran melebihi 2 juta
    if monthly_total > 2000000:
        st.error("Sudah mencapai batasan!")
