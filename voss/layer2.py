from __future__ import annotations

import re

from base.network_objects import Interface, MacAddresses, State, Connection
from voss import TechFile, VOSS


@TechFile.parser("show lldp neighbor")
def get_lldp_neighbors(text_lines: list[str]) -> dict[Interface, dict[str, VOSS.Object]]:
    """
    parse the output of "show lldp neighbor" and create structured data correlating
    the local port name with the lldp neighbor hostname and remote port name

    :param text_lines: the output of "show lldp neighbor" seperated by lines
    :return: a dictionary holding lldp neighbor hostnames and remote port indexed by port names
    """
    data = {}
    port: Interface | None = None
    for line in text_lines:
        port_name = re.search(r'Port: *\d+/\d+', line)
        if re.search(r'Port: *\d+/\d+', line):
            # We have found a line indicating the beginning of some LLDP neighbor information
            # Extract the local port name from this line and enter it in the data table
            port = Interface(port_name[0].replace("Port: ", ""))
            data.update({port: {}})
        elif "SysName" in line:
            # This line contains hostname (SysName) information
            # Grab the SysName. It is the last word on the line.
            if not port:
                continue
            data[port]["LLDP Remote SysName"] = Connection(line.split()[-1].strip())
        elif "PortId" in line:
            # This line contains remote port information
            # Grab the port name. It is the last word in the line.
            data[port]["LLDP Remote Interface"] = Interface(line.split()[-1].strip())
            pass
    return data


@TechFile.parser("show isis adjacencies")
def get_isis_adjacencies(text_lines: list[str]) -> dict[Interface, dict[str, VOSS.Object]]:
    """
    parse the output of "show isis adjacencies" and create structured data correlating
    the local port name with the isis neighbor hostname and adjacency status.

    :param text_lines: the output of "show isis adjacencies" seperated by lines
    :return: a dictionary holding isis neighbor hostnames and adjacency status indexed by port names
    """
    data: dict[Interface, dict] = {}
    for line in text_lines:
        port_name = re.search(r'Port\d+/\d+', line)
        if port_name:
            # We have found a line indicating some isis adjacency information
            port = Interface(port_name[0].replace("Port", ""))
            adj = re.search(r'([\w-]+)', line.split()[-2])[0]
            status = re.search(r'(\w+)', line.split()[-1])[0]
            data.update({port: {"ISIS Adjacency": Connection(adj), "ISIS Status": State(status)}})
    return data


@TechFile.parser("show interfaces gigabitEthernet")
def get_port_state(text_lines: list[str]) -> dict[Interface, dict[str, VOSS.Object]]:
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
                data.update({Interface(port_name):
                    {
                        "State": State("Up" if "up" in line else "Down"),
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
                port_name = Interface(match[0].replace("Port-", ""))
                mac = mac_pattern.search(line)[0]
                if port_name in data:
                    data[port_name]["MAC Addresses"].append(mac)
    # Convert MAC Address lists to MacAddresses objects for comparisons
    data = {port: {**data[port], "MAC Addresses": MacAddresses(data[port]["MAC Addresses"])} for port in data}
    return data
