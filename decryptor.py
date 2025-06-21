import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# Simulasi kunci tetap (ambil dari ransomware GUI)
DECRYPTION_KEY = b'MbXkzMmJ5dGVzc3VwZXJzZWNyZXRrZXlzdHJpbmchIQ=='

# Ekstensi file yang dienkripsi
ENCRYPTED_EXT = '.enc'

def decrypt_file(file_path, fernet):
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        decrypted = fernet.decrypt(data)

        # Hapus .enc dari nama file
        original_path = file_path.replace(ENCRYPTED_EXT, "")
        with open(original_path, "wb") as file:
            file.write(decrypted)

        os.remove(file_path)
        return True
    except Exception as e:
        print(f"Gagal dekripsi: {file_path} → {e}")
        return False

def process_decrypt(user_key):
    try:
        fernet = Fernet(user_key.encode())
    except Exception as e:
        messagebox.showerror("Key Error", f"Kunci tidak valid!\n{e}")
        return

    folder = filedialog.askdirectory()
    if not folder:
        return

    count = 0
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(ENCRYPTED_EXT):
                file_path = os.path.join(root, file)
                if decrypt_file(file_path, fernet):
                    count += 1

    if count > 0:
        messagebox.showinfo("Sukses", f"{count} file berhasil didekripsi.")
    else:
        messagebox.showwarning("Tidak Ada", "Tidak ada file terenkripsi ditemukan atau key salah.")

def launch_gui():
    root = tk.Tk()
    root.title("File Decryptor")
    root.geometry("400x200")

    tk.Label(root, text="Masukkan Kunci Dekripsi:", font=("Arial", 11)).pack(pady=10)

    key_entry = tk.Entry(root, width=50, show="*")
    key_entry.pack(pady=5)

    def on_decrypt_click():
        user_key = key_entry.get().strip()
        if user_key:
            process_decrypt(user_key)
        else:
            messagebox.showwarning("Kosong", "Kunci dekripsi harus diisi!")

    tk.Button(root, text="Dekripsi File", command=on_decrypt_click).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
