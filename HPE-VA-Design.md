# TABLE OF CONTENTS	
# LIST OF TABLES	
# LIST OF FIGURES	
## 1.	INTRODUCTION	
###    1.1.	REQUIREMENT	
    As an end customer I should be able to register all my devices (ILO/Storage/Network) to the HPE Connected Enterprise Systems, so that any fault occurs on my hardware there is a SFDC case is automatically created for immediate attention. And this should happen for more than 1000+ devices.
 

## 2.	SOLUTION OVERVIEW
    Discover all the devices using OpsRamp’s NextGen auto discovery capability, may be using the SNMP Traps (v1/v2/v3).
    Write an automation build that will read these devices and filter out the ILOs out of huge list of the discovered devices.
    Get the Admin credentials for each of ILO.
    Onboard these devices on the OneView.
    Register OneView to HPE Connected Systems Enterprise (there are pre-requisites for this that are to be met, which I am not aware of).
    Enable OVRS service in OneView.

###   2.1.  Architecture
###   2.2.  Data Flow
###   2.5.	SOLUTION COMPONENTS
####       2.5.1.	Virtual Appliance
####       2.5.2.	Embedded Kubernetes in Appliance
####       2.5.3.	Embedded KVM in Appliance

###    2.6.	Virtual Appliance CONFIGURATION	
####    2.6.1.	Networking Requirements for Virtual Appliance	
###    2.7.	Virtual Appliance LICENSE INFORMATION	
###    2.8.	Customer DEPENDENCIES & Prerequisites	
###    2.9.	ASSUMPTIONS	16
###    2.10.	Virtual Appliance DESIGN DECISIONS	

## 3.	Virtual Appliance TECHNICAL SPECIFICATIONS	
###    3.1.	Virtual Appliance INFRASTRUCTURE	
###    3.2.	Virtual Applliace SERVER SPECIFICATION	
####        3.2.1.	Kubernetes Cluster
####        3.2.3.	KVM
####        3.2.4.  OneView
####        3.2.5.  OpsRamp NextGen
####        3.2.6.  pFsense
####        3.2.7.  ServiceNow MidServer
####        3.2.8.  UXUI Interface

## 4.	END USER SERVICE EXPERIENCE
###    4.1.    DISASTER RECOVERY
####        4.1.1.	CMP Application Tier
####        4.1.2.	CMP Transactional DB Tier
####        4.1.3.	DR Failover/Failback approach
###    4.3.	BACKUPS
###    4.4.	SCALABILITY
###    4.5.	MAINTENANCE
####        4.5.1.	Patching & Upgrade

## 6.	CLOUD INTEGRATIONS AND SERVICE CATALOGS	32
###    6.1.	VMWARE VCENTER INTEGRATION	33
####        6.1.1.	Pre-requisites	33
####        6.1.2.	Catalogs	33
###    6.2.	MICROSOFT AZURE INTEGRATION	34
####        6.2.1.	Prerequisites	34
####        6.2.2.	Catalogs	35
###    6.3.	NSX INTEGRATION	35
####        6.3.1.	Prerequisites	35
####        6.3.2.	Catalogs	36
###    6.4.	NUTANIX	37
####        6.4.1.	Prerequisites	37
####        6.4.2.	Catalogs	37
###    6.5.	HPE MS ITSM	38
####        6.5.1.	Prerequisites	38
####        6.5.2.	Workflow Details	38

## 7.	SECURITY	39
###    7.1.	USER ACCOUNTS	39
###    7.2.	SERVICE ACCOUNTS	39
###    7.3.	ACCOUNT PERMISSIONS	39

## 8.  ORDERING PROCESS OF APPLIANCE

# APPENDIX A
# DOCUMENT SIGN-OFF

```
opsramp-collector-start install --environment k8s –-url {OpsRamp Server URL} –-key {Gateway unique authentication token} --proxy-protocol {Proxy Protocol http/https} --proxy-ip {Proxy IP Address} --proxy-port {Proxy Port} --config {YAML Discovery Configuration File Path}
```