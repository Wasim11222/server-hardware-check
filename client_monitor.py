import requests
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

# Konfiguration
SERVER_IP = "172.20.10.14"  # IP deines Servers
SENDER_EMAIL = "Wasimhajmhajmoustafa@gmail.com"
ADMIN_EMAIL = "Wasimhajmhajmoustafa@gmail.com"
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email_to_admin(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ADMIN_EMAIL
    try:
        if not SENDER_PASSWORD:
            raise ValueError("EMAIL_PASSWORD environment variable is not set!")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Admin wurde benachrichtigt.")
    except Exception as e:
        print(f"❌ Fehler beim Senden der E-Mail: {e}")

def get_server_data():
    try:
        response = requests.get(f"http://{SERVER_IP}:5000/status", timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def check_alerts(data):
    alerts = []
    if data.get("cpu_temp", 0) > 90:
        alerts.append("🔥 CPU Temperatur über 90°C!")
    if data.get("ram_percent", 0) >= 100:
        alerts.append("💾 RAM ist voll!")
    if data.get("disk_percent", 0) > 80:
        alerts.append("💽 SSD-Auslastung über 80%!")
    if data.get("net_sent_mb", 0) < 5 and data.get("net_recv_mb", 0) < 5:
        alerts.append("📡 Netzwerkaktivität unter 5 MB!")
    if alerts:
        send_email_to_admin("⚠️ Server-Warnung!", "\n".join(alerts))

def update_gui():
    global running
    if running:
        data = get_server_data()
        output = []

        if "error" in data:
            output.append("❌ Verbindung fehlgeschlagen:\n" + data["error"])
        else:
            output.append("🖥️ SERVER STATUS:")
            output.append(f"🌡️ CPU-Temp: {data['cpu_temp']} °C")
            output.append(f"💾 RAM:       {data['ram_percent']} %")
            output.append(f"💽 SSD:       {data['disk_percent']} %")
            output.append(f"📡 Gesendet:  {data['net_sent_mb']} MB")
            output.append(f"📡 Empfangen: {data['net_recv_mb']} MB")
            check_alerts(data)

        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, "\n".join(output))
        text_area.config(state=tk.DISABLED)

        try:
            interval = int(interval_entry.get()) * 1000
            root.after(interval, update_gui)
        except ValueError:
            text_area.insert(tk.END, "\n⚠️ Ungültiger Intervallwert!")
            toggle_monitoring()

def toggle_monitoring():
    global running
    running = not running
    if running:
        toggle_button.config(text="⏹️ Stop", bg="#f44336")
        update_gui()
    else:
        toggle_button.config(text="▶️ Start", bg="#4CAF50")

# GUI
root = tk.Tk()
root.title("🖥️ Server Monitor (Remote)")
root.geometry("600x600")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
text_area.pack(expand=True, fill='both', padx=10, pady=10)
text_area.config(state=tk.DISABLED)

interval_frame = tk.Frame(root)
interval_frame.pack(pady=5)

tk.Label(interval_frame, text="⏱️ Intervall (Sekunden):").pack(side=tk.LEFT)
interval_entry = tk.Entry(interval_frame, width=6)
interval_entry.pack(side=tk.LEFT)

toggle_button = tk.Button(root, text="▶️ Start", command=toggle_monitoring, font=("Arial", 12), bg="#4CAF50", fg="white")
toggle_button.pack(pady=10)

running = False
root.mainloop()
