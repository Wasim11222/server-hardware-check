from flask import Flask, jsonify
import psutil
import wmi

app = Flask(__name__)

@app.route('/status')
def get_status():
    data = {}
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                data["cpu_temp"] = round(sensor.Value, 1)
                break
    except:
        data["cpu_temp"] = None

    data["ram_percent"] = psutil.virtual_memory().percent
    data["disk_percent"] = psutil.disk_usage("/").percent
    net = psutil.net_io_counters()
    data["net_sent_mb"] = net.bytes_sent // (1024 ** 2)
    data["net_recv_mb"] = net.bytes_recv // (1024 ** 2)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
