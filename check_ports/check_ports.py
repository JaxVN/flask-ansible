from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/check-ports', methods=['POST'])
def check_ports():
    data = request.json
    devices = data.get("devices")

    if not devices:
        return jsonify({"error": "Devices information is missing"}), 400

    results = []
    for device in devices:
        interface = device.get("interface")
        switch_ip = device.get("switch_ip")

        if not all([interface, switch_ip]):
            return jsonify({"error": f"Missing required fields for device {device}"}), 400

        command = [
            "ansible-playbook", "/ansible/check_ports.yml",
            "-i", "/ansible/inventory.ini",
            "--extra-vars", f"interface={interface} switch_ip={switch_ip}"
        ]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            results.append({"device": device, "output": result.stdout})
        except subprocess.CalledProcessError as e:
            results.append({"device": device, "error": str(e)})

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)