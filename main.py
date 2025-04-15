import os
import shutil
import sys
import argparse
import logging
from tqdm import tqdm
from tkinter import Tk, filedialog, Button, Label, Checkbutton, IntVar, ttk
import datetime

# --- File categories ---
FILE_CATEGORIES = {
    "Documents": ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
    "Videos": ['.mp4', '.mkv', '.avi', '.mov'],
    "Music": ['.mp3', '.wav', '.aac'],
    "Code": ['.py', '.java', '.cpp', '.html', '.css', '.js'],
    "Archives": ['.zip', '.rar', '.7z', '.tar'],
    "Executables": ['.exe', '.msi', '.apk'],
    "Others": []
}

# --- Logging setup (IN CURRENT DIR) ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "autosortify.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Unique file naming
def get_unique_path(dest_folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(dest_folder, filename)
    while os.path.exists(new_path):
        new_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
        counter += 1
    return new_path

# Main logic
def organize_files(folder_path, dry_run=False, copy_files=False):
    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path.")
        logging.error(f"Invalid folder path: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(f"📂 Organizing {len(files)} files in: {folder_path}\n")

    summary = {cat: 0 for cat in FILE_CATEGORIES}
    summary["Others"] = 0

    for file_name in tqdm(files, desc="Organizing", ncols=70, colour='cyan'):
        file_path = os.path.join(folder_path, file_name)
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        moved = False

        for category, extensions in FILE_CATEGORIES.items():
            if ext in extensions:
                dest_folder = os.path.join(folder_path, category)
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = get_unique_path(dest_folder, file_name)

                if dry_run:
                    print(f"[DRY-RUN] Would move {file_name} → {category}/")
                    logging.info(f"[DRY-RUN] {file_name} → {category}/")
                else:
                    try:
                        if copy_files:
                            shutil.copy2(file_path, dest_path)
                        else:
                            shutil.move(file_path, dest_path)
                        logging.info(f"Moved {file_name} → {category}/")
                    except Exception as e:
                        logging.error(f"Failed to move {file_name}: {e}")
                summary[category] += 1
                moved = True
                break

        if not moved:
            dest_folder = os.path.join(folder_path, "Others")
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = get_unique_path(dest_folder, file_name)

            if dry_run:
                print(f"[DRY-RUN] Would move {file_name} → Others/")
                logging.info(f"[DRY-RUN] {file_name} → Others/")
            else:
                try:
                    if copy_files:
                        shutil.copy2(file_path, dest_path)
                    else:
                        shutil.move(file_path, dest_path)
                    logging.info(f"Moved {file_name} → Others/")
                except Exception as e:
                    logging.error(f"Failed to move {file_name} to Others: {e}")
            summary["Others"] += 1

    # Summary report
    if not dry_run:
        summary_file = os.path.join(HOME_DIR, "AutoSortify", "summary.txt")
        with open(summary_file, 'w') as f:
            f.write(f"📋 Summary Report ({datetime.datetime.now()}):\n\n")
            for cat, count in summary.items():
                f.write(f"{cat}: {count} files\n")
        print("\n✅ Summary saved in summary.txt")

    print("\n🎉 Done organizing! Check the log for details.")

# GUI
def launch_gui():
    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            organize_files(
                folder_selected,
                dry_run=dry_var.get(),
                copy_files=copy_var.get()
            )
            label.config(text="✅ Done! Check logs & summary.")


    root = Tk()
    root.title("AutoSortify")
    root.geometry("420x250")
    root.resizable(False, False)

    style = ttk.Style(root)
    theme_var = IntVar()
    dry_var = IntVar()
    copy_var = IntVar()

    Label(root, text="📁 Select a folder to organize", font=("Arial", 14)).pack(pady=10)
    Button(root, text="Browse Folder", command=browse_folder, width=20).pack(pady=5)
    Checkbutton(root, text="Dry Run (Preview Only)", variable=dry_var).pack()
    Checkbutton(root, text="Copy Instead of Move", variable=copy_var).pack()
    label = Label(root, text="", fg="green")
    label.pack(pady=5)

    root.mainloop()

# CLI
def cli():
    parser = argparse.ArgumentParser(description="AutoSortify - Smart File Organizer")
    parser.add_argument("folder", nargs="?", help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving")
    args = parser.parse_args()

    if args.folder:
        organize_files(args.folder, dry_run=args.dry_run, copy_files=args.copy)
    else:
        launch_gui()

if __name__ == "__main__":
    cli()
