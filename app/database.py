import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('devices.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            os TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_device(name, ip_address, username, password, os):
    conn = sqlite3.connect('devices.db')
    c = conn.cursor()
    password_hash = generate_password_hash(password)
    c.execute('''
        INSERT INTO devices (name, ip_address, username, password, os)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, ip_address, username, password_hash, os))
    conn.commit()
    conn.close()

def get_devices():
    conn = sqlite3.connect('devices.db')
    c = conn.cursor()
    c.execute('SELECT id, name, ip_address, username, os FROM devices')
    devices = c.fetchall()
    conn.close()
    return devices

def update_device(id, name, ip_address, username, password, os):
    conn = sqlite3.connect('devices.db')
    c = conn.cursor()
    password_hash = generate_password_hash(password)
    c.execute('''
        UPDATE devices
        SET name = ?, ip_address = ?, username = ?, password = ?, os = ?
        WHERE id = ?
    ''', (name, ip_address, username, password_hash, os, id))
    conn.commit()
    conn.close()

def delete_device(id):
    conn = sqlite3.connect('devices.db')
    c = conn.cursor()
    c.execute('DELETE FROM devices WHERE id = ?', (id,))
    conn.commit()
    conn.close()