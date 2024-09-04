import asyncio
from pysnmp.hlapi.v1arch.asyncio import *
import requests
import xmltodict
import sys
sys.path.insert(1, '/usr/local/lib/python3/dist-packages')

# Function to scan a range of IP addresses
def scan_ip_range(start_ip, end_ip, community):
    import ipaddress

    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)

    ilo_ips = []

    for ip_int in range(int(start_ip), int(end_ip) + 1):
        ip = str(ipaddress.IPv4Address(ip_int))
        print(f"Scanning {ip}...")

        try:
            response = requests.get(f"https://{ip}/xmldata?item=all",verify=False)
            response.raise_for_status()  # Raise an exception for HTTP errors
            if "iLO" in response.text:
                print("Found 'iLO' in the response.")
                ilo_ips.append(ip)
            else:
                print("Did not find 'iLO' in the response.")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

    print(ilo_ips)
    return ilo_ips

# Function to fetch iLO details via API
def fetch_ilo_details(ip, community):
    url = f"http://{ip}/xmldata?item=All"
    response = requests.get(url, auth=('admin', community), verify=False)
    xml_data = response.text
    return xmltodict.parse(xml_data)