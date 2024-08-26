from pysnmp.hlapi import *
import requests
import xmltodict

# Function to check if an IP address is an HPE iLO device using SNMP
def check_ilo(ip, community, oid="1.3.6.1.4.1.232"):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community, mpModel=1),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    return not error_indication and not error_status

# Function to scan a range of IP addresses
def scan_ip_range(start_ip, end_ip, community):
    import ipaddress

    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)

    ilo_ips = []

    for ip_int in range(int(start_ip), int(end_ip) + 1):
        ip = str(ipaddress.IPv4Address(ip_int))
        print(f"Scanning {ip}...")
        if check_ilo(ip, community):
            print(f"HPE iLO device found at IP: {ip}")
            ilo_ips.append(ip)
    
    return ilo_ips

# Function to fetch iLO details via API
def fetch_ilo_details(ip, community):
    url = f"http://{ip}/xmldata?item=All"
    response = requests.get(url, auth=('admin', community), verify=False)
    xml_data = response.text
    return xmltodict.parse(xml_data)
