from flask import Flask, render_template, request, redirect, url_for, jsonify
from discovery import scan_ip_range, fetch_ilo_details
from db import init_db, insert_ilo_data, get_all_ilo_data
import requests
import json

app = Flask(__name__)
# Initialize the database
init_db()

def get_ov_api_version():
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    oneview_ip="10.56.73.2"

    version_url = f"https://{oneview_ip}/rest/version"
    print(version_url)

    try:
        response = requests.get(version_url, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), response.status_code

    # Parse the response JSON to get the version
    ov_api_version = response.json().get("currentVersion")

    print(ov_api_version)
    return ov_api_version

def get_ov_session_id(current_version):
    oneview_ip="10.56.73.2"
    # Construct the URL    
    login_url = f"https://{oneview_ip}/rest/login-sessions"

    # Construct the payload
    payload = {
        "authLoginDomain":"Local",
        "password":"Admin@123",
        "userName":"Administrator",
        "loginMsgAck": "true"
    }

    # Define headers
    headers = {
        "X-Api-Version": f"{current_version}",
        "Content-Type": "application/json"
    }
    # POST request to the OneView API
    try:
        response = requests.post(login_url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), response.status_code

    # Parse the response JSON to get the session ID
    ov_session_id = response.json().get("sessionID")
    print(ov_session_id)
    
    return ov_session_id


@app.route("/")
def home():
    return render_template("base.html")

@app.route('/ilo', methods=['GET', 'POST'])
def ilo():
    if request.method == 'POST':
        start_ip = request.form['start_ip']
        end_ip = request.form['end_ip']
        community = request.form['community']

        # Discover iLO IPs
        ilo_ips = scan_ip_range(start_ip, end_ip, community)

        # Fetch and store details for each discovered iLO device
        for ilo_ip in ilo_ips:
            xml_data = fetch_ilo_details(ilo_ip, community)
            print(xml_data)
            insert_ilo_data(ilo_ip, xml_data)

        return redirect(url_for('results'))

    return render_template('ilo.html')


# Storage Devices
@app.route('/storage', methods=['GET', 'POST'])
def storage():
    if request.method == 'POST':
        start_ip = request.form['start_ip']
        end_ip = request.form['end_ip']
        community = request.form['community']

    return render_template('storage.html')

# Network Devices
@app.route('/network', methods=['GET', 'POST'])
def network():
    if request.method == 'POST':
        start_ip = request.form['start_ip']
        end_ip = request.form['end_ip']
        community = request.form['community']

    return render_template('network.html')

@app.route('/results', methods=['GET'])
def results():
    ilo_data = get_all_ilo_data()
    return render_template('results.html', ilo_data=ilo_data)

@app.route('/register', methods=['GET','POST'])
def register():
    # Disable SSL warnings (insecure)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    
    oneview_ip="10.56.73.2"

    # Step-1: Fetch Current OneView Version 
    version_url = f"https://{oneview_ip}/rest/version"
    print(version_url)

    try:
        response = requests.get(version_url, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), response.status_code

    # Parse the response JSON to get the version
    current_version = response.json().get("currentVersion")

    if not current_version:
        return jsonify({"error": "Failed to retrieve current version"}), 500

    print(current_version)

    # Step-2 Fetch OneView Login Session Id
    # Construct the URL    
    login_url = f"https://{oneview_ip}/rest/login-sessions"

    # Construct the payload
    payload = {
        "authLoginDomain":"Local",
        "password":"Admin@123",
        "userName":"Administrator",
        "loginMsgAck": "true"
    }

    # Define headers
    headers = {
        "X-Api-Version": f"{current_version}",
        "Content-Type": "application/json"
    }
    # POST request to the OneView API
    try:
        response = requests.post(login_url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), response.status_code

    # Parse the response JSON to get the session ID
    session_id = response.json().get("sessionID")
    print(session_id)

    if not session_id:
        return jsonify({"error": "Failed to retrieve session ID"}), 500
    
    # Step-3a: Fetch the details from the results page and construct a loop to run through all the iLOs
    ips = request.form.getlist('ip[]')
    ers = request.form.getlist('ers[]')
    usernames = request.form.getlist('ilousername[]')
    passwords = request.form.getlist('ilopasswd[]')

     # Combine the data into a list of dictionaries
    table_data = []
    for i in range(len(ips)):
        table_data.append({
            'ip': ips[i],
            'ers': ers[i],
            'username': usernames[i],
            'password': passwords[i]
        })
    print(table_data)
    # Step-3b: Add Server HW (Rack Mount Only) to OneView
    add_ilo_url = f"https://{oneview_ip}/rest/server-hardware"

    # Construct the payload
    for row in table_data:
        payload = { 
            "hostname" : f"{row['ip']}", 
            "username" : f"{row['username']}", 
            "password" : f"{row['password']}", 
            "force" : "true", 
            "licensingIntent":"OneViewStandard",
            "configurationState":"Monitored"
        }

        # Define headers
        headers = {
            "X-Api-Version": f"{current_version}",
            "Content-Type": "application/json",
            "Auth": f"{session_id}"
        }
        # POST request to the OneView API
        try:
            response = requests.post(add_ilo_url, json=payload, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            return jsonify({"error": str(err)}), response.status_code

        if response.status_code != 202:
            return jsonify({"error": "Failed to add iLO"}), 500

    return jsonify(table_data)

def hpersdetails():
    rs_data = []
    ov_fqdn_ip="10.56.73.2"
    url = f"https://{ov_fqdn_ip}/rest/support/configuration"

    ov_api_version = get_ov_api_version()

    if not ov_api_version:
        return jsonify({"error": "Failed to retrieve current version"}), 500
    
    ov_session_id = get_ov_session_id(ov_api_version)
    if not ov_session_id:
        return jsonify({"error": "Failed to retrieve session Id"}), 500

    # Define headers
    headers = {
        "X-Api-Version": f"{ov_api_version}",
        "Auth": f"{ov_session_id}",
        "Content-Type": "application/json"
    }
    # POST request to the OneView API
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), response.status_code

    rs_data.append(jsonify(response.text))
    return render_template('hpersdetails.html',rs_data=rs_data)

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)

## FOR Reference: cURL for adding Server HardWare to OneView
# curl -XPOST -k https://10.56.73.2/rest/login-sessions \
# -H 'X-Api-Version: 6000' \
# -H 'Content-Type: application/json' \
# -d '{
#       "userName":"Administrator",  
#       "password":"Admin@123", 
#       "loginMsgAck": "true"
#     }'