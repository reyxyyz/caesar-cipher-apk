import streamlit as st

# Fungsi Caesar Cipher
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

# Streamlit App
st.title("🔐 Caesar Cipher App")

st.write("""
Aplikasi ini menggunakan Caesar Cipher untuk **enkripsi** dan **dekripsi** pesan.
""")

# Input dari pengguna
option = st.selectbox("Pilih Mode", ("Enkripsi", "Dekripsi"))
text = st.text_area("Masukkan Teks:")
shift = st.slider("Geser (Shift)", min_value=1, max_value=25, value=3)

# Tombol Proses
if st.button("Proses"):
    if option == "Enkripsi":
        hasil = caesar_encrypt(text, shift)
        st.success(f"Hasil Enkripsi:\n{hasil}")
    else:
        hasil = caesar_decrypt(text, shift)
        st.success(f"Hasil Dekripsi:\n{hasil}")

