# 🚀 AutoSortify

### A smart Python file organizer that de-clutters your folders with one command.

---

## ⚡ Features

- 🧠 Auto-categorizes files (Documents, Images, Code, etc.)
- 💻 Built-in GUI using Tkinter for easier use
- 🕒 Scheduler-ready via cron/Task Scheduler
- 📊 Real-time progress bar using `tqdm`
- 📝 Logs actions to `autosortify.log`
- 🔧 Clean folder structure & robust error handling

---

## 📦 File Categories

| Category     | Extensions                                        |
|--------------|---------------------------------------------------|
| Documents    | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx`         |
| Images       | `.jpg`, `.jpeg`, `.png`, `.svg`, `.gif`           |
| Videos       | `.mp4`, `.mkv`, `.avi`, `.mov`                    |
| Music        | `.mp3`, `.wav`, `.aac`                            |
| Code         | `.py`, `.cpp`, `.java`, `.js`, `.html`, `.css`    |
| Archives     | `.zip`, `.rar`, `.7z`, `.tar`                     |
| Executables  | `.exe`, `.msi`, `.apk`                            |
| Others       | Everything else                                   |

---

## 🧠 How It Works

AutoSortify scans the specified folder, detects file types based on extension, and moves them into clean, categorized subfolders like:

---

## 📌 Usage

### 1. Clone the repo

```bash
git clone https://github.com/your-username/AutoSortify.git
cd AutoSortify
```
### 2. Run the script

```bash
python main.py /path/to/your/folder
```
---

## 📅 Setup Scheduled Run (Optional)
### Windows Task Scheduler:
- Open Task Scheduler → Create Basic Task
- Trigger: Daily/Weekly
- Action: Start a Program → python path_to_main.py "C:/Your/Folder"

---

## 📄 Logs
All operations are saved in autosortify.log with timestamps, success/failure, and file movements.






