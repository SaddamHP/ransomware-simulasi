import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Simulasi kunci tetap (harus sama dengan yang digunakan oleh ransomware)
# Jika kamu ingin biarkan user input bebas, jangan pakai DECRYPTION_KEY
ENCRYPTED_EXT = '.enc'

# Folder-folder target otomatis yang dipindai untuk file terenkripsi
TARGET_DIRS = [
    os.path.expanduser("~/vmshare"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads")
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
        print(f"✅ Didekripsi: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Gagal dekripsi: {file_path} → {e}")
        return False

def process_decrypt(user_key):
    try:
        fernet = Fernet(user_key.encode())
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

    tk.Label(root, text="Masukkan Kunci Dekripsi:", font=("Arial", 11)).pack(pady=15)

    key_entry = tk.Entry(root, width=55, show="*")
    key_entry.pack(pady=5)

    def on_decrypt_click():
        user_key = key_entry.get().strip()
        if user_key:
            process_decrypt(user_key)
        else:
            messagebox.showwarning("Kosong", "Kunci dekripsi harus diisi!")

    tk.Button(root, text="🛠 Dekripsi Semua File", command=on_decrypt_click).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
