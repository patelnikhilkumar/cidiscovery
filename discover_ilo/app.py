from flask import Flask, render_template, request, redirect, url_for
from discovery import scan_ip_range, fetch_ilo_details
from db import init_db, insert_ilo_data, get_all_ilo_data
import requests

app = Flask(__name__)
OV_USERNAME="Administrator"
OV_PASSWORD="Admin@123"


# Initialize the database
init_db()

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

@app.route('/register')
def register():
    OV_IP="10.56.73.2" 
    OV_URI=f"https://{OV_IP}/rest/login-sessions"

    headers = {
        "X-Api-Version":"6000",
        "Content-Type": "application/json"
    }
    data = {
        "authLoginDomain":"Local",
        "password":"Admin@123",
        "userName":"Administrator",
        "loginMsgAck": "true"
    }

    response = requests.post(OV_URI, data=data, headers=headers)
    print(response)
    return render_template('register.html',response=response)

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)


# Create Network and Network Sets
# Network Sets:
#     Inside that you will have multiple networks

# Logical Interconnect Groups

# curl -XPOST -k https://10.56.73.2/rest/login-sessions -H 'X-Api-Version: 6000' -H 'Content-Type: application/json' -d '{"userName":"Administrator",  "password":"Admin@123", "loginMsgAck": "true"}'