import sqlite3

DATABASE = 'ilo_devices.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ilo_devices
                      (ip TEXT PRIMARY KEY, 
                       server_name TEXT, 
                       product_name TEXT, 
                       serial_number TEXT, 
                       firmware_version TEXT)''')
    conn.commit()
    conn.close()

# Insert iLO data into the database
def insert_ilo_data(ip, xml_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    ilo_info = xml_data['RIMP']['MP']
    server_name = ilo_info.get('SBSN', 'Unknown')
    product_name = ilo_info.get('PN', 'Unknown')
    serial_number = ilo_info.get('SPN', 'Unknown')
    firmware_version = ilo_info.get('FWRI', 'Unknown')

    cursor.execute('''INSERT OR REPLACE INTO ilo_devices 
                      (ip, server_name, product_name, serial_number, firmware_version) 
                      VALUES (?, ?, ?, ?, ?)''',
                   (ip, server_name, product_name, serial_number, firmware_version))
    
    conn.commit()
    conn.close()

# Retrieve all iLO data from the database
def get_all_ilo_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ilo_devices')
    rows = cursor.fetchall()
    conn.close()
    return rows
