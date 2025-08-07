# Smart File Organizer - Full Version
from tkinter import filedialog, messagebox, StringVar, Text, Frame, Label, Button, Entry, Tk, WORD, END, BOTH, LEFT, RIGHT, X
import os
import shutil
import threading
import sqlite3
from playsound import playsound

# --- Organize files ---
def organize_files(folder_path, log_callback):
    if not os.path.exists(folder_path):
        log_callback("Folder not found.\n")
        return

    files = os.listdir(folder_path)
    if not files:
        log_callback("No files found in the folder.\n")
        return

    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext[1:].lower() or "others"
            ext_folder = os.path.join(folder_path, ext)

            if not os.path.exists(ext_folder):
                os.makedirs(ext_folder)

            try:
                shutil.move(file_path, os.path.join(ext_folder, file))
                log_callback(f"Moved: {file} → {ext}/\n")
                log_to_database(file, ext)
            except Exception as e:
                log_callback(f"Error moving {file}: {str(e)}\n")
    log_callback("Organization complete.\n")

# --- Log to SQLite database ---
def log_to_database(file_name, file_type):
    conn = sqlite3.connect('file_organizer.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_logs
                 (file_name TEXT, file_type TEXT)''')
    c.execute("INSERT INTO file_logs (file_name, file_type) VALUES (?, ?)", (file_name, file_type))
    conn.commit()
    conn.close()

# --- Upload to Google Drive ---
def upload_to_drive():
    try:
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            file_drive = drive.CreateFile({'title': file_name})
            file_drive.SetContentFile(file_path)
            file_drive.Upload()
            messagebox.showinfo("Upload", f"{file_name} uploaded to Google Drive.")
    except Exception as e:
        messagebox.showerror("Upload Failed", str(e))

# --- Splash screen ---
def show_splash(main_callback):
    splash = Tk()
    splash.overrideredirect(True)
    w, h = 400, 200
    x = (splash.winfo_screenwidth() - w) // 2
    y = (splash.winfo_screenheight() - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")

    Label(splash, text="Loading Smart File Organizer...", font=("Arial", 14, "bold")).pack(expand=True)

    def play_sound():
        try:
            playsound("welcome.wav")
        except Exception as e:
            print("Sound error:", e)

    threading.Thread(target=play_sound, daemon=True).start()
    splash.after(2000, lambda: [splash.destroy(), main_callback()])
    splash.mainloop()

# --- Main GUI ---
def launch_gui():
    app = Tk()
    app.title("Smart File Organizer")
    app.geometry("800x500")
    app.minsize(600, 400)

    screen_w = app.winfo_screenwidth()
    screen_h = app.winfo_screenheight()
    x = (screen_w - 800) // 2
    y = (screen_h - 500) // 2
    app.geometry(f"+{x}+{y}")

    messagebox.showinfo("Welcome", "Welcome to Smart File Organizer!")

    theme = {"bg": "white", "fg": "black"}

    def apply_theme():
        app.configure(bg=theme["bg"])
        log_area.configure(bg=theme["bg"], fg=theme["fg"])
        status.configure(bg=theme["bg"], fg=theme["fg"])
        folder_frame.configure(bg=theme["bg"])
        drag_drop_btn.configure(bg=theme["bg"], fg=theme["fg"])
        organize_btn.configure(bg="#4CAF50", fg="white")
        bottom.configure(bg=theme["bg"])
        for widget in folder_frame.winfo_children():
            widget.configure(bg=theme["bg"], fg=theme["fg"])

    def toggle_theme():
        if theme["bg"] == "white":
            theme.update({"bg": "#222222", "fg": "white"})
        else:
            theme.update({"bg": "white", "fg": "black"})
        apply_theme()

    def log(msg):
        log_area.insert(END, msg)
        log_area.see(END)

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_path.set(folder)
            log(f"Selected: {folder}\n")

    def handle_organize():
        path = folder_path.get()
        if not path:
            messagebox.showwarning("No Folder", "Please select a folder first.")
            return
        log("Organizing files...\n")
        organize_files(path, log)

    folder_path = StringVar()
    folder_frame = Frame(app, bg=theme["bg"])
    folder_frame.pack(pady=10)

    folder_entry = Entry(folder_frame, textvariable=folder_path, width=60)
    folder_entry.pack(side=LEFT, padx=5)
    Button(folder_frame, text="Browse Folder", command=browse_folder).pack(side=LEFT)

    def drop_files():
        files = filedialog.askopenfilenames()
        if files:
            dropped_folder = os.path.dirname(files[0])
            folder_path.set(dropped_folder)
            log(f"Dragged files from: {dropped_folder}\n")

    drag_drop_btn = Button(app, text="📂 Drag & Drop or Browse", command=drop_files)
    drag_drop_btn.pack(pady=5)

    organize_btn = Button(app, text="🧹 Organize Files", command=handle_organize, bg="#4CAF50", fg="white", padx=10)
    organize_btn.pack(pady=5)

    log_area = Text(app, height=15, wrap=WORD)
    log_area.pack(fill=BOTH, expand=True, padx=10, pady=10)

    bottom = Frame(app, bg=theme["bg"])
    bottom.pack(fill=X, pady=5)

    status = Label(bottom, text="Ready", anchor="w", bg=theme["bg"], fg=theme["fg"])
    status.pack(side=LEFT, padx=10)

    Button(bottom, text="Upload to Drive", command=upload_to_drive).pack(side=RIGHT, padx=5)
    Button(bottom, text="Toggle Theme", command=toggle_theme).pack(side=RIGHT, padx=5)
    Button(bottom, text="Exit", command=app.destroy).pack(side=RIGHT)

    apply_theme()
    app.mainloop()

# --- Run App ---
show_splash(launch_gui)
