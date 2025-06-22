import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Key tetap yang sesuai dengan ransomware kamu
DECRYPTION_KEY = 'cHZhczJ2cWtQam5Sd1R0Y3Z0a1RQZ1h2TnU1TFY5bWE='
ENCRYPTED_EXT = '.enc'

# Folder-folder target
TARGET_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    "Z:\\vmshare"
]

def decrypt_file(file_path, fernet):
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        decrypted = fernet.decrypt(data)

        original_path = file_path.replace(ENCRYPTED_EXT, "")
        with open(original_path, "wb") as file:
            file.write(decrypted)

        os.remove(file_path)
        print(f"Didekripsi: {file_path}")
        return True
    except Exception as e:
        print(f"Gagal dekripsi: {file_path} → {e}")
        return False

def process_decrypt():
    try:
        fernet = Fernet(DECRYPTION_KEY.encode())
    except Exception as e:
        messagebox.showerror("Key Error", f"Kunci tidak valid!\n{e}")
        return

    total = 0
    for folder in TARGET_DIRS:
        if not os.path.exists(folder):
            continue

        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(ENCRYPTED_EXT):
                    file_path = os.path.join(root, file)
                    if decrypt_file(file_path, fernet):
                        total += 1

    if total > 0:
        messagebox.showinfo("Sukses", f"{total} file berhasil didekripsi!")
    else:
        messagebox.showwarning("Tidak Ada", "Tidak ada file .enc ditemukan atau kunci salah.")

def launch_gui():
    root = tk.Tk()
    root.title("🔐 File Decryptor Otomatis")
    root.geometry("420x220")

    tk.Label(root, text="Kunci dekripsi sudah dimasukkan otomatis.", font=("Arial", 11)).pack(pady=20)
    tk.Button(root, text="Dekripsi Semua File", command=process_decrypt).pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
