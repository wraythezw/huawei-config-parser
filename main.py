import re
import json

# Function to parse the configuration export from a file
def parse_config(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Sample Huawei router config export file path
config_file = "router_config.txt"
config_export = parse_config(config_file)

# Initialize an empty list to store interface dictionaries
interfaces = []

# Regular expressions to extract information from each line
interface_regex = re.compile(r'interface (\S+)\.(\d+)')
description_regex = re.compile(r' description (.+)')
state_regex = re.compile(r'shutdown')
bandwidth_regex = re.compile(r' bandwidth (\d+)')
vrf_regex = re.compile(r' ip binding vpn-instance (\S+)')
ip_regex = re.compile(r' ip address (\S+) (\S+)')
qos_regex = re.compile(r' qos-profile (\S+) (inbound|outbound)')

# Iterate through each line in the config export
interface_id = None
interface_vlan = None
interface_dict = {}
for line in config_export.split('\n'):
    interface_match = interface_regex.match(line)
    if interface_match:
        interface_id = interface_match.group(1)
        interface_vlan = interface_match.group(2)
        interface_dict = {'interface_id': interface_id, 'interface_vlan': interface_vlan, 'interface_state':'active'}

    description_match = description_regex.match(line)
    if description_match:
        interface_dict['description'] = description_match.group(1)

    if state_regex.search(line):
        interface_dict['interface_state'] = 'shutdown'


    bandwidth_match = bandwidth_regex.match(line)
    if bandwidth_match:
        interface_dict['bandwidth'] = int(bandwidth_match.group(1))

    vrf_match = vrf_regex.match(line)
    if vrf_match:
        interface_dict['vrf'] = vrf_match.group(1)

    ip_match = ip_regex.match(line)
    if ip_match:
        interface_dict['ip4_addr'] = ip_match.group(1)
        interface_dict['ip4_mask'] = ip_match.group(2)

    qos_match = qos_regex.match(line)
    if qos_match:
        qos_direction = qos_match.group(2)
        if qos_direction == 'inbound':
            interface_dict['qos_inbound'] = qos_match.group(1)
        else:
            interface_dict['qos_outbound'] = qos_match.group(1)
    if line == '#':
        if(interface_dict):
            interfaces.append(interface_dict)
            interface_id = None
            interface_vlan = None
            interface_dict = {}
# Generate JSON dictionary
json_dict = {'interfaces': interfaces}


# File path to write JSON data
file_path = "output.json"

# Write JSON data to file
with open(file_path, "w") as file:
    json.dump(json_dict, file, indent=4)