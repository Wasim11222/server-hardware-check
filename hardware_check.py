# 📦 Bibliotheken-Importe
import psutil                     # Für Systeminformationen (CPU, RAM, Festplatte etc.)
import platform                   # Betriebssystem-Informationen (derzeit nicht genutzt)
import subprocess                 # Zum Ausführen von externen Programmen (nicht genutzt)
import tkinter as tk              # GUI-Toolkit
from tkinter import scrolledtext  # Für scrollbaren Textbereich in der GUI
from datetime import datetime     # Für Zeitstempel im Log
import smtplib                    # E-Mail-Versand
from email.mime.text import MIMEText  # Formatierung der E-Mail
import os                         # Umgebungsvariablen (z.B. Passwort auslesen)

# ---------------- E-Mail Konfiguration ----------------
ADMIN_EMAIL = "Wasimhajmhajmoustafa@gmail.com"        # Empfänger der Warnmeldungen
SENDER_EMAIL = "Wasimhajmhajmoustafa@gmail.com"       # Absender der E-Mail (gleicher Account)
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")         # Passwort aus Umgebungsvariable

# 🔹 Funktion zum Versenden einer E-Mail bei Fehlern oder Warnungen
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

# 🔹 CPU-Temperatur auslesen (funktioniert nur mit OpenHardwareMonitor)
def get_cpu_temperature():
    try:
        import wmi
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        sensors = w.Sensor()
        temps = []
        for sensor in sensors:
            if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                temps.append(sensor.Value)
        return temps if temps else [0.0]
    except Exception as e:
        return [0.0]

# 🔹 CPU-Informationen abrufen
def get_cpu_info():
    cpu_freq = psutil.cpu_freq()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    usage = psutil.cpu_percent(interval=1)
    return [
        f"🧠 CPU-Info:",
        f"   Cores: {cpu_cores}, Threads: {cpu_threads}",
        f"   Frequenz: {cpu_freq.current:.2f} MHz",
        f"   Auslastung: {usage}%",
    ]

# 🔹 RAM-Nutzung auslesen
def get_ram_info():
    ram = psutil.virtual_memory()
    return ram.percent, [
        f"💾 RAM:",
        f"   Gesamt: {ram.total // (1024 ** 2)} MB",
        f"   Verfügbar: {ram.available // (1024 ** 2)} MB",
        f"   Nutzung: {ram.percent}%",
    ]

# 🔹 Festplattenauslastung auslesen
def get_disk_info():
    disk = psutil.disk_usage('/')
    return disk.percent, [
        f"💽 Speicher (SSD/HDD):",
        f"   Gesamt: {disk.total // (1024 ** 3)} GB",
        f"   Genutzt: {disk.used // (1024 ** 3)} GB",
        f"   Frei: {disk.free // (1024 ** 3)} GB",
        f"   Auslastung: {disk.percent}%",
    ]

# 🔹 Netzwerkaktivität abrufen
def get_network_info():
    net = psutil.net_io_counters()
    sent = net.bytes_sent // (1024 ** 2)
    recv = net.bytes_recv // (1024 ** 2)
    return sent, recv, [
        f"📡 Netzwerk:",
        f"   Gesendet: {sent} MB",
        f"   Empfangen: {recv} MB",
    ]

# 🔹 Warnungen prüfen und ggf. E-Mail an Admin senden
def check_alerts(cpu_temp, ram_percent, disk_percent, net_sent, net_recv):
    alerts = []
    if any(t > 90 for t in cpu_temp):
        alerts.append("🔥 CPU Temperatur über 90°C!")
    if ram_percent >= 100:
        alerts.append("💾 RAM ist voll!")
    if disk_percent > 80:
        alerts.append("💽 SSD-Auslastung über 80%!")
    if net_sent < 5 and net_recv < 5:
        alerts.append("📡 Netzwerkaktivität unter 5 MB!")

    if alerts:
        send_email_to_admin("⚠️ Server-Warnung!", "\n".join(alerts))

# 🔹 Daten in eine Logdatei schreiben
def log_to_file(lines):
    with open("hardware_log.txt", "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file.write(f"\n{timestamp}\n")
        file.write("\n".join(lines) + "\n")

# 🔁 Daten abrufen, anzeigen, loggen und überwachen
def update_gui():
    global running
    if running:
        output = []

        # CPU
        output.extend(get_cpu_info())
        cpu_temp = get_cpu_temperature()
        output.append(f"🌬️ CPU-Temperatur: {cpu_temp[0]:.1f}°C")
        output.append("")

        # RAM
        ram_percent, ram_info = get_ram_info()
        output.extend(ram_info)
        output.append("")

        # Festplatte
        disk_percent, disk_info = get_disk_info()
        output.extend(disk_info)
        output.append("")

        # Netzwerk
        net_sent, net_recv, net_info = get_network_info()
        output.extend(net_info)

        # Anzeige in GUI aktualisieren
        text_area.config(state=tk.NORMAL)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "\n".join(output))
        text_area.config(state=tk.DISABLED)

        # Logging & Warnungen
        log_to_file(output)
        check_alerts(cpu_temp, ram_percent, disk_percent, net_sent, net_recv)

        # Wiederholung nach angegebenem Intervall
        try:
            interval = int(interval_entry.get()) * 1000  # Sekunden in Millisekunden
            root.after(interval, update_gui)
        except ValueError:
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, "\n⚠️ Fehler: Ungültiger Intervallwert!\n")
            text_area.config(state=tk.DISABLED)
            toggle_monitoring()

# ▶️ Start / ⏹️ Stop der Überwachung
def toggle_monitoring():
    global running
    running = not running
    if running:
        toggle_button.config(text="⏹️ Stop", bg="#f44336")
        update_gui()
    else:
        toggle_button.config(text="▶️ Start", bg="#4CAF50")

# 🔹 GUI-Elemente erstellen
root = tk.Tk()
root.title("🖥️ Server Hardware Monitor")
root.geometry("600x600")

# Textfeld für Ausgabe
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
text_area.pack(expand=True, fill='both', padx=10, pady=10)
text_area.config(state=tk.DISABLED)

# Eingabe für Intervallzeit
interval_frame = tk.Frame(root)
interval_frame.pack(pady=5)

tk.Label(interval_frame, text="⏱️ Intervall (Sekunden):").pack(side=tk.LEFT)
interval_entry = tk.Entry(interval_frame, width=6)
interval_entry.pack(side=tk.LEFT)

# Start/Stop Button
toggle_button = tk.Button(
    root,
    text="▶️ Start",
    command=toggle_monitoring,
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white"
)
toggle_button.pack(pady=10)

# Überwachungsstatus-Flag
running = False

# GUI starten
root.mainloop()
