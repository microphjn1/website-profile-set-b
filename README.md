SET-B prototype — run & restart instructions (Windows PowerShell)

This README explains how to open, run, and restart the Flask application, how to start ngrok for public access, and where uploaded images are stored.

Prerequisites
- Windows (PowerShell)
- Python 3.8+ installed and on PATH
- (Optional) ngrok.exe placed in the project folder or installed globally

Project location (example)
C:\Users\admin\Desktop\Website Set-b prototype-20251104T071513Z-1-001\Website Set-b prototype

Quick start (first time)
1. Open PowerShell and change to the project folder:

```powershell
cd "C:\Users\admin\Desktop\Website Set-b prototype-20251104T071513Z-1-001\Website Set-b prototype"
```

2. Create a virtual environment (if you don't already have one):

```powershell
python -m venv .venv
```

3. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies (if present). If the repository contains a `requirements.txt`, run:

```powershell
pip install -r requirements.txt
```

If there is no `requirements.txt`, install the minimal packages:

```powershell
pip install flask
# optional (recommended) for server-side image validation and ngrok usage:
pip install pillow pyngrok
```

Run the server

1. From the activated venv, start the Flask app:

```powershell
python main.py
```

2. The server binds to port 5000. You should see messages like:

* Running on http://127.0.0.1:5000

3. Open http://127.0.0.1:5000 (or http://localhost:5000) in your browser.

Start ngrok (optional — expose site publicly)

1. If you have `ngrok.exe` in the project folder, run:

```powershell
ngrok http 5000
```

(or provide full path: `.
grok.exe http 5000`).

2. The ngrok terminal will print one or two "Forwarding" URLs (http and https). Copy the https URL and open it in a browser to access the site remotely.

3. To add your authtoken (only once):

```powershell
ngrok config add-authtoken <YOUR_AUTHTOKEN>
```

Stopping and restarting the server

- Stop the server that was started with `python main.py` by pressing Ctrl+C in that terminal.
- To start it again, re-run `python main.py` in the project folder with the venv activated.

If the server was started elsewhere or you need to kill a stray process:

1. Find the Python process (shows command line):

```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine
```

2. Kill a specific PID (replace <pid>):

```powershell
Stop-Process -Id <pid>
```

Notes on uploaded images

- Uploaded pictures are saved to: `static/uploads` (project root). Example absolute path:

  C:\Users\admin\Desktop\Website Set-b prototype-20251104T071513Z-1-001\Website Set-b prototype\static\uploads\<filename>

- The database stores the filename (or in some older records, an explicit static path). Templates generate URLs like `/static/uploads/<filename>` so uploaded pictures show in the student list and profile.

- If you add an image using the web form, check the `static/uploads` directory for the file and then refresh the home/profile page.

Troubleshooting

- Images not visible:
  - Make sure the Flask server was restarted after recent code changes.
  - Confirm the uploaded file exists in `static/uploads`.
  - Check the browser devtools Network tab for the image request and its HTTP status (404 means file missing).

- Search box not preserving value:
  - Use the search form at /home. Enter a term and submit; the input will show the query after the page reload.

- ngrok URL not reachable:
  - Make sure ngrok is running in a terminal and your Flask server is running on port 5000.
  - Copy the exact forwarding URL shown in the ngrok terminal (long names can wrap in the terminal; copy the full URL).

Security notes

- Uploaded files are accepted if the browser reports an image MIME type. For greater safety consider:
  - Adding server-side validation (e.g., using Pillow to open & re-save images),
  - Normalizing filenames (prefix with UUIDs to avoid collisions),
  - Sanitizing or restricting SVG uploads.

If you want, I can add a small script to normalize/validate existing images and a command to run it.

----
Generated on: 2025-11-06
