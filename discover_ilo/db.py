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
                       firmware_version TEXT,
                       remote_support TEXT,
                       health_status TEXT)''')
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
                      (ip, server_name, server_type, product_name, serial_number, firmware_version, remote_support, health_status) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
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

# {
#     'RIMP': 
#     {'HSI': 
#         {'SBSN': 'SGH632XWFC', 
#          'SPN': 'ProLiant DL380 Gen9', 
#          'UUID': '719061SGH632XWFC', 
#          'SP': '1', 
#          'cUUID': '30393137-3136-4753-4836-333258574643', 
#          'VIRTUAL': 
#             {
#                 'STATE': 'Inactive', 
#                 'VID':
#                     {
#                         'BSN': None, 
#                         'cUUID': None
#                     }
#             }, 
#             'PRODUCTID': '719061-B21', 
#             'NICS': {
#                 'NIC': [
#                     {
#                         'PORT': '1', 
#                         'DESCRIPTION': 'iLO 4', 
#                         'LOCATION': 'Embedded', 
#                         'MACADDR': 'e0:07:1b:f8:88:36', 
#                         'IPADDR': '10.66.63.35', 
#                         'STATUS': 'OK'
#                     }, 
#                     {
#                         'PORT': '2', 
#                         'DESCRIPTION': 'iLO 4', 
#                         'LOCATION': 'Embedded', 
#                         'MACADDR': 'e0:07:1b:f8:88:37', 
#                         'IPADDR': 'Unknown', 
#                         'STATUS': 'Disabled'
#                     }, 
#                     {
#                         'PORT': '1', 
#                         'DESCRIPTION': 'HPE Ethernet 1Gb 4-port 331i Adapter - NIC', 
#                         'LOCATION': 'Embedded', 
#                         'MACADDR': '1c:98:ec:15:7f:8c', 
#                         'IPADDR': None, 
#                         'STATUS': 'Unknown'
#                     }, 
#                     {
#                         'PORT': '2', 
#                         'DESCRIPTION': 'HPE Ethernet 1Gb 4-port 331i Adapter - NIC', 
#                         'LOCATION': 'Embedded', 
#                         'MACADDR': '1c:98:ec:15:7f:8d', 
#                         'IPADDR': None, 
#                         'STATUS': 'Unknown'
#                     }, 
#                     {
#                         'PORT': '3', 
#                         'DESCRIPTION': 'HPE Ethernet 1Gb 4-port 331i Adapter - NIC', 
#                         'LOCATION': 'Embedded', 
#                         'MACADDR': '1c:98:ec:15:7f:8e', 
#                         'IPADDR': None, 
#                         'STATUS': 'Unknown'
#                     }, 
#                     {
#                         'PORT': '4', 
#                         'DESCRIPTION': 
#                         'HPE Ethernet 1Gb 4-port 331i Adapter - NIC', 
#                         'LOCATION': 'Embedded', 
#                         'MACADDR': '1c:98:ec:15:7f:8f', 
#                         'IPADDR': None, 
#                         'STATUS': 'Unknown'
#                     }
#                 ]
#             }
#         }, 
#     'MP': {
#         'ST': '1', 
#         'PN': 'Integrated Lights-Out 4 (iLO 4)', 
#         'FWRI': '2.80', 
#         'BBLK': None, 
#         'HWRI': 'ASIC: 17', 
#         'SN': 'ILOSGH632XWFC', 
#         'UUID': 'ILO719061SGH632XWFC', 
#         'IPM': '1', 
#         'SSO': '1', 
#         'PWRM': '1.0.9', 
#         'ERS': '0', 
#         'EALERT': '1'
#         }, 
#     'SPATIAL': {
#         'DISCOVERY_RACK': 
#         'Not Supported', 
#         'DISCOVERY_DATA': 'Server does not detect Location Discovery Services', 
#         'TAG_VERSION': '0', 
#         'RACK_ID': '0', 
#         'RACK_ID_PN': '0', 
#         'RACK_DESCRIPTION': '0', 
#         'RACK_UHEIGHT': '0', 
#         'UPOSITION': '0', 
#         'ULOCATION': '0', 
#         'cUUID': '30393137-3136-4753-4836-333258574643', 
#         'UHEIGHT': '2.00', 
#         'UOFFSET': '0'
#         }, 
#     'HEALTH': {
#         'STATUS': '2'
#         }
#     }
# }
