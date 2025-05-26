import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ===== Caesar Cipher Functions =====
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ===== Database Setup =====
DB_NAME = "caesar_cipher.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cipher_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT,
            input_text TEXT,
            shift INTEGER,
            result_text TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(mode, input_text, shift, result_text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO cipher_log (mode, input_text, shift, result_text, timestamp) VALUES (?, ?, ?, ?, ?)",
              (mode, input_text, shift, result_text, timestamp))
    conn.commit()
    conn.close()

def fetch_history():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM cipher_log ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# ===== Streamlit App =====
st.title("🔐 Caesar Cipher App + Database + Tabel")

create_table()  # Buat tabel jika belum ada

st.write("Gunakan Caesar Cipher untuk mengenkripsi atau mendekripsi teks dan simpan hasilnya ke database.")

# Input
mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
text = st.text_area("Masukkan Teks:")
shift = st.slider("Geser (Shift)", 1, 25, 3)

# Proses
if st.button("Proses"):
    if mode == "Enkripsi":
        result = caesar_encrypt(text, shift)
    else:
        result = caesar_decrypt(text, shift)

    st.success(f"Hasil {mode}:\n{result}")
    insert_record(mode, text, shift, result)
    st.info("✅ Hasil berhasil disimpan ke database.")

# Tampilkan Tabel Riwayat
st.subheader("📊 Tabel Riwayat Enkripsi/Dekripsi")
history_df = fetch_history()

if not history_df.empty:
    st.dataframe(history_df)
else:
    st.write("Belum ada data riwayat.")
