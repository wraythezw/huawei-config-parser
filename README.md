# huawei-config-parser

## Introduction
This is a simple python script to parse a huawei config file and generate a json 'definition' of the configuration file.

#### Current working features

- Interfaces


#### Planned

- Routing
- VRF Definitions
- QOS Profiles
- ?
- cli args
- bulk processing

## 
### Usage
    cp /path/to/routerconfig ./router_config.txt
    python3 main.py

#### Output sample
        [
            {
                "interface_id": "GigabitEthernet0/2/27",
                "interface_vlan": "4010",
                "interface_state": "active",
                "description": "Test Interface",
                "bandwidth": 20,
                "qos_inbound": "20M",
                "qos_outbound": "20M"
            }
        ]