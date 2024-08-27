import sqlite3

DATABASE = 'ilo_devices.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ilo_devices
                      (ip TEXT PRIMARY KEY, 
                       server_name TEXT,
                       server_type TEXT,
                       product_name TEXT, 
                       serial_number TEXT, 
                       firmware_version TEXT
                       remote_support TEXT
                       health_status TEXT''')
    conn.commit()
    conn.close()

# Insert iLO data into the database
def insert_ilo_data(ip, xml_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    ilo_info = xml_data['RIMP']['MP']
    ilo_info2 = xml_data['RIMP']['HSI']
    ilo_info3 = xml_data['RIMP']['HEALTH']

    server_name = ilo_info2.get('SBSN', 'Unknown')
    server_type = ilo_info2.get('SPN', 'Unknown')
    product_name = ilo_info.get('PN', 'Unknown')
    serial_number = ilo_info.get('SN', 'Unknown')
    firmware_version = ilo_info.get('FWRI', 'Unknown')
    remote_support = ilo_info.get('ERS', 'Unknown')
    health_status = ilo_info3.get('STATUS', 'Unknown')


    cursor.execute('''INSERT OR REPLACE INTO ilo_devices 
                      (ip, server_name, server_type, product_name, serial_number, firmware_version, remote_support) 
                      VALUES (?, ?, ?, ?, ?)''',
                   (ip, server_name, server_type, product_name, serial_number, firmware_version, remote_support, health_status))
    
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
