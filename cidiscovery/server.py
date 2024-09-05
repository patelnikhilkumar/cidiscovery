from flask import Flask, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import time
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hpecidetails.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create Table: cmdb_ci_vm_instance
class Cmdb_ci_hpeilo_instance(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(250), nullable=True)
    make                = db.Column(db.String(64), nullable=True)
    model               = db.Column(db.Integer, nullable=True)
    os                  = db.Column(db.Float, nullable=True)
    ip_address          = db.Column(db.Integer, nullable=True)
    is_ers_enabled      = db.Column(db.Integer, nullable=True)
    disksizeobjectid    = db.Column(db.String(128), nullable=True)

with app.app_context():
    db.create_all()

# new_cmdb_ci = Cmdb_ci_vm_instance(
#     name             = "opsramplinuxgw-JR",
#     state            = "POWERED_OFF",
#     vcpus            = 4,
#     memory           = 16384,
#     disk             = 128
# )

# db.session.add(new_cmdb_ci)
# db.session.commit()

def get_details():
    dc_count = db.session.query(Cmdb_ci_vm_instance.id).count()
    esx_count = db.session.query(Cmdb_ci_vm_instance.id).count()
    vm_count = db.session.query(Cmdb_ci_vm_instance.id).count()
    ds_count = db.session.query(Cmdb_ci_vm_instance.id).count()

    vir_details = [dc_count,esx_count,vm_count,ds_count]
    return vir_details

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/vir")
def vmwaredetails():

    all_vms = Cmdb_ci_vm_instance.query.order_by(Cmdb_ci_vm_instance.id).all()
    for i in range(len(all_vms)):
        all_vms[i].ranking = len(all_vms) - i
    db.session.commit()

    vir_details = get_details()
    return render_template("vir.html", vmlist=all_vms, dc_count=vir_details[0], esx_count=vir_details[1],vm_count=vir_details[2], ds_count=vir_details[3])

@app.route("/vms")
def vminstances():

    all_vms = Cmdb_ci_vm_instance.query.order_by(Cmdb_ci_vm_instance.id).all()
    for i in range(len(all_vms)):
        all_vms[i].ranking = len(all_vms) - i
    db.session.commit()
    vir_details = get_details()
    return render_template("vms.html", vmlist=all_vms, dc_count=vir_details[0], esx_count=vir_details[1],vm_count=vir_details[2], ds_count=vir_details[3])


@app.route("/esxi")
def esxi():

    all_vms = Cmdb_ci_vm_instance.query.order_by(Cmdb_ci_vm_instance.id).all()
    for i in range(len(all_vms)):
        all_vms[i].ranking = len(all_vms) - i
    db.session.commit()
    vir_details = get_details()
    return render_template("esxi.html", vmlist=all_vms,dc_count=vir_details[0], esx_count=vir_details[1],vm_count=vir_details[2], ds_count=vir_details[3])

## Code to do the bulk refresh
@app.route("/refresh", methods=["GET","POST","DELETE"])
def refresh():

    ## Calling vCenter API to fetch the details of VMs
    vm_url = "https://api.npoint.io/f41e57d550e8be836336"
    response = requests.get(vm_url)
    all_vms = response.json()

    for i in range(len(all_vms)):
        new_cmdb_ci = Cmdb_ci_vm_instance(
            name             = all_vms[i]["name"],
            state            = all_vms[i]["power_state"],
            vcpus            = all_vms[i]["cpu_count"],
            memory           = all_vms[i]["memory_size_MiB"],
            disk             = 128
        )
        db.session.add(new_cmdb_ci)
    db.session.commit()
 
    return redirect('/vms')

# Storage Routes
@app.route("/storage")
def show_storage():
    return render_template('storage.html')

@app.route("/nimble_main")
def display_nimble_main():
    return render_template('nimble_main.html', arr_count=0,pools_count=0,vol_count=0)

@app.route("/arrays")
def display_arrays():
    return render_template('nimble_array.html',arr_count=0,pools_count=0,vol_count=0)

@app.route("/pools")
def display_pools():
    return render_template('nimble_pools.html',arr_count=0,pools_count=0,vol_count=0)

@app.route("/vols")
def display_volumes():
    return render_template('nimble_volume.html',arr_count=0,pools_count=0,vol_count=0)

@app.route('/api/v1/dummy')
def return_json():
    dummy={
        "fname": "Nikhil",
        "lname": "Patel",
        "username": "n007",
        "age": 39
    }
    return jsonify(dummy)
if __name__ == '__main__':
    app.run(debug=True)
