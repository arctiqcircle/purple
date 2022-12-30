import re

from typing import Any
from dynex import Port
from voss import VOSS


@VOSS.parser("show interfaces gigabitEthernet")
def get_port_state(text_lines: list[str]) -> dict[Port, dict[str, Any]]:
    """
    parse the output of "show interfaces gigabitEthernet" and create a table correlating
    the port name and the port status

    :param text_lines: the output of "show interfaces gigabitEthernet" seperated by lines
    :return: a dictionary holding port states indexed by port names
    """
    data = {}
    pattern = re.compile(r'\d+\/\d+')
    searching_state = False
    portmac_pattern = re.compile(r'Port-\d+\/\d+')
    searching_mac = False
    mac_pattern = re.compile(r'(?:[0-9a-fA-F](:|\.)?){12}')


    for line in text_lines:
        if "Port Name" in line: # We found the section we want.
            searching_state = True
        elif "Port Config" in line: # We reached the next section. Stop searching.
            searching_state = False
        if searching_state:
            match = pattern.search(line)
            if match:
                port_name = match[0]
                data.update({Port(port_name):
                    {
                        "State": 'up' in line,
                        "MAC Addresses": []
                    }
                })


        if "Port Fdb" in line: #Begin searching for MAC Addresses 
            searching_mac = True
        elif "Brouter Port Ip" in line:
            searching_mac = False
        if searching_mac:
            match = portmac_pattern.search(line)
            if match:
                port_name = Port(match[0].replace("Port-",""))
                mac = mac_pattern.search(line)[0]
                if port_name in data:
                    data[port_name]["MAC Addresses"].append(mac)
    return data
