import psutil
import platform
import subprocess
import tkinter as tk
from tkinter import scrolledtext

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

def get_cpu_temperature():
    try:
        import wmi
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        sensors = w.Sensor()
        temps = []
        for sensor in sensors:
            if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                temps.append(f"🌬️ CPU-Temperatur: {sensor.Value:.1f}°C")
        return temps if temps else ["🌬️ CPU-Temperatur: Keine Daten (OpenHardwareMonitor muss laufen)"]
    except Exception as e:
        return [f"🌬️ CPU-Temperatur konnte nicht gelesen werden: {e}"]

def get_ram_info():
    ram = psutil.virtual_memory()
    return [
        f"💾 RAM:",
        f"   Gesamt: {ram.total // (1024 ** 2)} MB",
        f"   Verfügbar: {ram.available // (1024 ** 2)} MB",
        f"   Nutzung: {ram.percent}%",
    ]

def get_disk_info():
    disk = psutil.disk_usage('/')
    return [
        f"💽 Speicher (SSD/HDD):",
        f"   Gesamt: {disk.total // (1024 ** 3)} GB",
        f"   Genutzt: {disk.used // (1024 ** 3)} GB",
        f"   Frei: {disk.free // (1024 ** 3)} GB",
        f"   Auslastung: {disk.percent}%",
    ]

def get_network_info():
    net = psutil.net_io_counters()
    return [
        f"📡 Netzwerk:",
        f"   Gesendet: {net.bytes_sent // (1024 ** 2)} MB",
        f"   Empfangen: {net.bytes_recv // (1024 ** 2)} MB",
    ]

def show_results(title, lines):
    root = tk.Tk()
    root.title(title)
    root.geometry("550x500")
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
    text_area.pack(expand=True, fill='both')
    text_area.insert(tk.END, "\n".join(lines))
    text_area.config(state=tk.DISABLED)
    root.mainloop()

def check_hardware():
    results = []
    results.extend(get_cpu_info())
    results.extend(get_cpu_temperature())
    results.append("")  # Leerzeile
    results.extend(get_ram_info())
    results.append("")
    results.extend(get_disk_info())
    results.append("")
    results.extend(get_network_info())
    show_results("🖥️ Server-Hardware Check", results)

# Starte das Skript
check_hardware()
