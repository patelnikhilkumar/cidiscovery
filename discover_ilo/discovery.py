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
            else:
                print("Did not find 'iLO' in the response.")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

        # if asyncio.run(check_ilo(ip, community)):
        #     print(f"HPE iLO device found at IP: {ip}")
        #     ilo_ips.append(ip)

        print(ilo_ips)

    return ilo_ips

# Function to fetch iLO details via API
def fetch_ilo_details(ip, community):
    url = f"http://{ip}/xmldata?item=All"
    response = requests.get(url, auth=('admin', community), verify=False)
    xml_data = response.text
    return xmltodict.parse(xml_data)

# def check_ilo_in_response(u):
#     url = "https://10.66.63.11/xmldata?item=all"
#     try:
#         response = requests.get(url,verify=False)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         if "iLO" in response.text:
#             print("Found 'iLO' in the response.")
#         else:
#             print("Did not find 'iLO' in the response.")
#     except requests.exceptions.RequestException as err:
#         print(f"Request Exception: {err}")

# Function to check if an IP address is an HPE iLO device using SNMP
# async def check_ilo(ip, community, oid="1.3.6.1.4.1.232"):
#     errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
#         SnmpDispatcher(),
#         CommunityData(community),
#         UdpTransportTarget((ip, 161)),
#         ObjectType(ObjectIdentity(oid))
#     )
#     print(errorIndication, errorStatus, errorIndex, varBinds)

#     return not errorIndication and not errorStatus

    # error_indication, error_status, error_index, var_binds = next(
    #     getCmd(snmpDispatcher(),
    #            CommunityData(community, mpModel=1),
    #            UdpTransportTarget((ip, 161)),
    #            ContextData(),
    #            ObjectType(ObjectIdentity(oid)))
    # )

    # return not error_indication and not error_status