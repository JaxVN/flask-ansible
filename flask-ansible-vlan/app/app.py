from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/change-vlan', methods=['POST'])
def change_vlan():
    data = request.json
    interface = data.get("interface")
    vlan_id = data.get("vlan_id")
    switch_ip = data.get("switch_ip")

    if not all([interface, vlan_id, switch_ip]):
        return jsonify({"error": "Missing required fields"}), 400

    # Run the Ansible Playbook
    command = [
        "ansible-playbook", "ansible/playbook.yml",
        "-i", "ansible/inventory.ini",
        "--extra-vars", f"interface={interface} vlan_id={vlan_id} switch_ip={switch_ip}"
    ]

    try:
        subprocess.run(command, check=True)
        return jsonify({"message": "VLAN updated successfully!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
