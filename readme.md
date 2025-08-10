# Local File Transfer System (LFTS)

A simple **local network file sharing and management system** built with Flask. Easily share files between your PC and phone (or any device on the same network) without cables or third-party apps.

---

## Features

- Browse files and folders in a shared directory via web browser  
- Upload files directly from your device  
- Download files to your device with a clean UI  
- Create, rename, and delete files and folders  
- Responsive and mobile-friendly design  
- Secure path handling to prevent directory traversal  
- Customizable max upload size (default 2000MB)  
- Minimal terminal output for clean startup  
- Custom terminal banner (with fallback for executable builds)  

---

## Benefits

- **No cables or USB drives needed** — transfer files over WiFi or LAN  
- **Cross-platform** — works on any device with a modern browser (Windows, Android, iOS, Linux)  
- **Lightweight** — uses Python and Flask, no heavy software required  
- **Easy to use** — intuitive web interface accessible from any browser  
- **Safe and secure** — prevents access outside the shared folder  
- **Fully open source** — customize as you like  
---

## Safety and Security

This software is **harmless** and runs entirely on your local network. It does **not** send your files or data anywhere else, and does **not** include any tracking, ads, or malware. It simply provides a secure way to share files between your devices on the same network.

---

## Who Should Install This

This software is ideal for users who want to transfer files between devices on the same local network without using cables, cloud services, or third-party applications. If you want a simple, self-hosted file manager accessible from your phone or other devices, this is for you.

---
## Requirements

- **Python 3.7+**  
- Python packages (install via pip):  
  - Flask  
  - pyfiglet  
  - colorama  

You can install dependencies with this command:
```bash
# create a virtual environment and activate it before installing requirements (optional)
pip install -r requirements.txt
```
## How to Use

### After Downloading the Executable (.exe)

1. **Download** the latest executable from here:  
 [Download LFTS](https://github.com/madin-prime/LocalFileTransferSystem/releases/download/0.1/LocalFileTransferSystem.exe.zip)

2. **Place the executable file** (`LFTS.exe` or your named `.exe`) anywhere on your PC.

3. **Run the executable** by double-clicking it.  
   - A terminal window will open showing a welcome banner and instructions.

4. **Find your PC’s local IP address**:  
   - On Windows, open Command Prompt and run `ipconfig` to find the IPv4 address (usually something like `192.168.x.x`).  
   - On macOS/Linux, open Terminal and run `ifconfig` or `ip a`.

5. **On your phone or other device connected to the same WiFi/network**, open a web browser and enter:

