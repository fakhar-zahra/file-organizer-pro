import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import logging

# Setup logging
logging.basicConfig(filename="organizer_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
}

def organize_files(folder_path, progress_var):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)

    for idx, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)
        _, ext = os.path.splitext(filename)
        moved = False

        for folder_name, extensions in file_types.items():
            if ext.lower() in extensions:
                folder_dest = os.path.join(folder_path, folder_name)
                if not os.path.exists(folder_dest):
                    os.makedirs(folder_dest)
                shutil.move(file_path, os.path.join(folder_dest, filename))
                logging.info(f"Moved {filename} to {folder_name}")
                moved = True
                break

        if not moved:
            others_path = os.path.join(folder_path, "Others")
            if not os.path.exists(others_path):
                os.makedirs(others_path)
            shutil.move(file_path, os.path.join(others_path, filename))
            logging.info(f"Moved {filename} to Others")

        progress = ((idx + 1) / total_files) * 100
        progress_var.set(progress)

    messagebox.showinfo("Done","Files organized successfully!")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        threading.Thread(target=start_organizing, args=(folder_selected,)).start()

def start_organizing(folder_path):
    progress_var.set(0)
    organize_files(folder_path, progress_var)

# ----------------------------- GUI -----------------------------
root = tk.Tk()
root.title("✨ File Organizer Pro ✨")
root.geometry("450x300")
root.configure(bg="#2c3e50")  # Dark background

label = tk.Label(
    root,
    text="Select Folder to Organize",
    font=("Helvetica", 16, "bold"),
    bg="#2c3e50",
    fg="#ecf0f1"
)
label.pack(pady=20)

btn = tk.Button(
    root,
    text="Browse Folder",
    command=select_folder,
    width=20,
    bg="#27ae60",
    fg="white",
    font=("Helvetica", 12, "bold"),
    activebackground="#2ecc71",
    cursor="hand2",
    relief="flat"
)
btn.pack(pady=10)

style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", thickness=20, troughcolor="#34495e", background="#27ae60", bordercolor="#2c3e50", lightcolor="#27ae60", darkcolor="#27ae60")

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300, style="TProgressbar")
progress_bar.pack(pady=20)

footer = tk.Label(
    root,
    text="Made with ❤️ using Python & Tkinter",
    font=("Helvetica", 10),
    bg="#2c3e50",
    fg="#95a5a6"
)
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
