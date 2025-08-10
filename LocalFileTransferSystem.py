import os
import sys
import logging
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, abort
import pyfiglet
from colorama import Fore, Style, init

banner = r"""
 _     _____ _____ ____  
| |   |  ___|_   _/ ___|
| |   | |_    | | \___ \
| |___|  _|   | |  ___) |
|_____|_|     |_| |____/
"""

# Suppress Flask/Werkzeug startup info logs, show only errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

BASE_DIR = os.path.abspath("shared_files")
os.makedirs(BASE_DIR, exist_ok=True)

# Optional: Increase max upload size to 100 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

def safe_path(path=""):
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    if not full_path.startswith(BASE_DIR):
        abort(403)  # prevent directory traversal
    return full_path

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def browse(path):
    abs_path = safe_path(path)
    if not os.path.exists(abs_path):
        return "Path does not exist", 404

    if os.path.isfile(abs_path):
        return redirect(url_for('download_file', path=path))

    items = os.listdir(abs_path)
    folders = []
    files = []

    for item in sorted(items):
        item_path = os.path.join(abs_path, item)
        rel_item_path = os.path.relpath(item_path, BASE_DIR).replace("\\", "/")
        if os.path.isdir(item_path):
            folders.append({"name": item, "rel_path": rel_item_path})
        else:
            files.append({"name": item, "rel_path": rel_item_path})

    parent_path = os.path.relpath(os.path.join(abs_path, ".."), BASE_DIR)
    if parent_path == ".":
        parent_path = ""

    return render_template("index.html",
                           current_path=path,
                           parent_path=parent_path,
                           folders=folders,
                           files=files)

@app.route("/download/<path:path>")
def download_file(path):
    abs_path = safe_path(path)
    if not os.path.isfile(abs_path):
        return "File not found", 404
    directory = os.path.dirname(abs_path)
    filename = os.path.basename(abs_path)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route("/upload/", defaults={"path": ""}, methods=["POST"])
@app.route("/upload/<path:path>", methods=["POST"])
def upload(path):
    abs_path = safe_path(path)
    if not os.path.isdir(abs_path):
        return "Upload path is not a folder", 400
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    save_path = os.path.join(abs_path, file.filename)
    try:
        file.save(save_path)
    except Exception as e:
        return f"Error saving file: {e}", 500

    return redirect(url_for('browse', path=path))

@app.route("/create_folder/", defaults={"path": ""}, methods=["POST"])
@app.route("/create_folder/<path:path>", methods=["POST"])
def create_folder(path):
    abs_path = safe_path(path)
    if not os.path.isdir(abs_path):
        return "Path is not a folder", 400

    folder_name = request.form.get('folder_name')
    if not folder_name:
        return "Folder name required", 400

    new_folder_path = os.path.join(abs_path, folder_name)
    try:
        os.makedirs(new_folder_path)
    except Exception as e:
        return f"Failed to create folder: {e}", 500

    return redirect(url_for('browse', path=path))

@app.route("/rename/", defaults={"path": ""}, methods=["POST"])
@app.route("/rename/<path:path>", methods=["POST"])
def rename(path):
    abs_path = safe_path(path)
    if not os.path.exists(abs_path):
        return "File/Folder not found", 404

    new_name = request.form.get("new_name")
    if not new_name:
        return "New name required", 400

    new_path = os.path.join(os.path.dirname(abs_path), new_name)
    try:
        os.rename(abs_path, new_path)
    except Exception as e:
        return f"Rename failed: {e}", 500

    parent_rel = os.path.relpath(os.path.dirname(abs_path), BASE_DIR)
    if parent_rel == ".":
        parent_rel = ""

    return redirect(url_for('browse', path=parent_rel))

@app.route("/delete/", defaults={"path": ""}, methods=["POST"])
@app.route("/delete/<path:path>", methods=["POST"])
def delete(path):
    abs_path = safe_path(path)
    if not os.path.exists(abs_path):
        return "File/Folder not found", 404

    try:
        if os.path.isfile(abs_path):
            os.remove(abs_path)
        else:
            import shutil
            shutil.rmtree(abs_path)
    except Exception as e:
        return f"Delete failed: {e}", 500

    parent_rel = os.path.relpath(os.path.dirname(abs_path), BASE_DIR)
    if parent_rel == ".":
        parent_rel = ""

    return redirect(url_for('browse', path=parent_rel))


if __name__ == "__main__":
    print(banner)
    print(Fore.CYAN + "🚀 " + Style.BRIGHT + "Starting File Manager Server...")
    print(Fore.YELLOW + "Open your phone browser and go to: http://<PC_IP_ADDRESS>:5000")
    print(Fore.RED+ "Run ipconfig on your terminal to know your pc's ip address")
    print(Fore.BLUE + "CTRL + C to close this program\n")

    app.run(host="0.0.0.0", port=5000, debug=False)
