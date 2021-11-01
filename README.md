# ACI Configuration Example

[![PyPI](https://img.shields.io/pypi/v/meraki-cli.svg)](https://pypi.python.org/pypi/meraki-cli)    
[![Python Versions](https://img.shields.io/pypi/pyversions/meraki-cli.svg)](https://pypi.python.org/pypi/meraki-cli)    
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/wafersystems/aci)

## Requirement

To use this code you will need

*	`Python` 3.6+
*	`Windows` operating system

## Preparation

Before execute scripts please modify some startup information in the two file below:

1. `login_info.py`: modify your `APIC` address and `username`/`password`
2. `startup_config.py`: modify some startup config(manual configed) such as `Tenants`, `AppProfiles`, `EPGS`, `Interface Policy Groups`. Examples are in the `startup_config.py`. 

## Usage

Two scripts are executable, `fabric_intprofile_setup.py` and `access_port_config.py`:

1. Fabric interfaces startup config. Create `Leaf Interface Profile` for every leaf switch and add `Access Port Selector` for every port under every leaf switch
Excute `fabric_intprofile_setup/fabric_intprofile_setup.py` to do configure, it will ask for leaf range(ex.101-108) and number of ports(ex.48) on every leaf on CMD

2. According to access requests given by other partners of `storage/virtualization/server`,  auto config the `Access Port Selector` and add description. For untag mode access machines, the codes first auto change the “Leaf Access Port Policy Group” which policy group attached an AEP without EPG recognizing, then codes config `static ports` under specific EPG.

* In `endpoint_access_config/accessrequest.csv` fill your access requests
* Excute `endpoint_access_config/access_port_config.py` to do configure
		
