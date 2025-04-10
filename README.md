# 🖥️ Remote Server Hardware Monitoring System

## 📌 Projektbeschreibung

Dieses Projekt ist ein client-server-basiertes System zur **Überwachung von Server-Hardware in Echtzeit** – lokal oder über das Netzwerk. Es überwacht automatisch die wichtigsten Ressourcen wie:

- CPU-Auslastung und Temperatur
- RAM-Nutzung
- Festplattenauslastung
- Netzwerkaktivität

Im Falle kritischer Schwellenwerte wird automatisch eine Warn-E-Mail an den Administrator gesendet.

---

## 🛠️ Projektbestandteile

Das Projekt besteht aus **drei Hauptkomponenten**:

### 🔹 1. `hardware_check.py` *(lokaler Hardwaremonitor)*

- Läuft auf dem Zielgerät (z. B. einem Server oder PC)
- Liest regelmäßig alle Hardwaredaten aus
- Zeigt die Werte in einer grafischen Benutzeroberfläche an (Tkinter)
- Schreibt die Daten in eine Datei: `hardware_log.txt`
- Sendet automatisch Warnungen per E-Mail bei kritischen Zuständen

> Dies ist ideal für **Standalone-Nutzung direkt am Gerät**.

### 🔹 2. `server_api.py` *(Server-Schnittstelle)*

- Läuft auf dem Server, den man aus der Ferne überwachen möchte
- Stellt eine einfache HTTP-API zur Verfügung (mittels Flask)
- Route: `/status` liefert aktuelle Systemdaten als JSON

> Dieses Skript macht den Server über das Netzwerk **fernabfragbar**.

### 🔹 3. `client_monitor.py` *(Client zur Fernüberwachung)*

- Läuft z. B. auf deinem Laptop
- Ruft regelmäßig die Daten vom Server über `/status` ab
- Zeigt die Ergebnisse in einer übersichtlichen GUI
- Erkennt kritische Zustände und benachrichtigt per E-Mail

---

## 💡 Wie funktioniert das?

### Beispiel-Ablauf:

1. **Auf dem Server**:
   - `server_api.py` wird gestartet → Der Server bietet die `/status`-API an
   - Optional: `hardware_check.py` kann parallel laufen, um lokal Logs zu speichern

2. **Auf dem Client/Laptop**:
   - `client_monitor.py` wird gestartet
   - Gibt die IP-Adresse des Servers an (`SERVER_IP`)
   - Holt Daten via HTTP → Zeigt diese an und sendet ggf. Warnungen

3. **E-Mail-Benachrichtigung**:
   - Wenn Temperatur, RAM, SSD-Auslastung oder Netzwerkaktivität kritisch sind, wird automatisch eine E-Mail an den Admin gesendet.

---

## 📂 Dateien im Projekt

| Datei                 | Beschreibung |
|----------------------|--------------|
| `hardware_check.py`  | Lokaler Monitor mit GUI, Logging, E-Mail-Warnung |
| `client_monitor.py`  | Remote-Client zur Fernüberwachung via Flask-API |
| `server_api.py`      | Flask-API zur Server-Datenbereitstellung |
| `hardware_log.txt`   | Gespeicherte Messdaten vom lokalen Monitor |
| `start_monitor.bat`  | Windows Batch-Datei zum Starten der Anwendung |
| `schreibtischtest.pdf` | Dokumentation der Temperaturfunktion |
| `sequenzdiagramm.png` | Darstellung der Kommunikation zwischen Client und Server |
| `Use-caseDiagramm.drawio.png` | Übersicht über Systemfunktionen und Benutzer |


## 🔧 Voraussetzungen

Damit das Projekt fehlerfrei läuft, müssen folgende Voraussetzungen erfüllt sein:

### 🐍 Python-Pakete

Installiere über pip:
```bash
pip install psutil flask wmi
