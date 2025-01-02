from flask import Flask, request, jsonify, render_template
import os
import subprocess
import json
from app.database import init_db, add_device, get_devices, update_device, delete_device

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices', methods=['GET', 'POST'])
def manage_devices():
    if request.method == 'POST':
        data = request.json
        name = data.get("name")
        ip_address = data.get("ip_address")
        username = data.get("username")
        password = data.get("password")
        os = data.get("os")
        add_device(name, ip_address, username, password, os)
        return jsonify({"message": "Device added successfully!"})
    else:
        devices = get_devices()
        return jsonify(devices)

@app.route('/devices/<int:id>', methods=['PUT', 'DELETE'])
def update_or_delete_device(id):
    if request.method == 'PUT':
        data = request.json
        name = data.get("name")
        ip_address = data.get("ip_address")
        username = data.get("username")
        password = data.get("password")
        os = data.get("os")
        update_device(id, name, ip_address, username, password, os)
        return jsonify({"message": "Device updated successfully!"})
    elif request.method == 'DELETE':
        delete_device(id)
        return jsonify({"message": "Device deleted successfully!"})

@app.route('/change-vlan', methods=['POST'])
def change_vlan():
    generate_inventory_file()
    data = request.json
    interface = data.get("interface")
    vlan_id = data.get("vlan_id")
    switch_ip = data.get("switch_ip")

    if not all([interface, vlan_id, switch_ip]):
        return jsonify({"error": "Missing required fields"}), 400

    # Run the Ansible Playbook
    command = [
        "ansible-playbook", "/ansible/playbook.yml",
        "-i", "/ansible/inventory.ini",
        "--extra-vars", f"interface={interface} vlan_id={vlan_id} switch_ip={switch_ip}"
    ]

    try:
        subprocess.run(command, check=True)
        return jsonify({"message": "VLAN updated successfully!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

def generate_inventory_file():
    devices = get_devices()
    with open('/ansible/inventory.ini', 'w') as f:
        f.write('[switches]\n')
        for device in devices:
            f.write(f'{device[1]} ansible_host={device[2]} ansible_user={device[3]} ansible_password={device[4]} ansible_network_os={device[5]}\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)