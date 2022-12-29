import re

from dynex import Port
from voss import VOSS


@VOSS.parser("show lldp neighbor")
def get_lldp_neighbors(text_lines: list[str]) -> dict[Port, dict[str, str]]:
    """
    parse the output of "show lldp neighbor" and create structured data correlating
    the local port name with the lldp neighbor hostname and remote port name

    :param text_lines: the output of "show lldp neighbor" seperated by lines
    :return: a dictionary holding lldp neighbor hostnames and remote port indexed by port names
    """
    data = {}
    for line in text_lines:
        port_name = re.search(r'Port: *\d+/\d+', line)
        if re.search(r'Port: *\d+/\d+', line):
            # We have found a line indicating the beginning of some LLDP neighbor information
            # Extract the local port name from this line and enter it in the data table
            port = Port(port_name[0].replace("Port: ", ""))
            data.update({port: {}})
        elif "SysName" in line:
            # This line contains hostname (SysName) information
            # Grab the SysName. It is the last word on the line.
            data[port]["LLDP Remote SysName"] = line.split()[-1].strip()
        elif "PortId" in line:
            # This line contains remote port information
            # Grab the port name. It is the last word in the line.
            data[port]["LLDP Remote Port"] = line.split()[-1].strip()
            pass
    return data


@VOSS.parser("show isis adjacencies")
def get_isis_adjacencies(text_lines: list[str]) -> dict[Port, dict[str, str]]:
    """
    parse the output of "show isis adjacencies" and create structured data correlating
    the local port name with the isis neighbor hostname and adjacency status.

    :param text_lines: the output of "show isis adjacencies" seperated by lines
    :return: a dictionary holding isis neighbor hostnames and adjacency status indexed by port names
    """
    data: dict[Port, dict] = {}
    for line in text_lines:
        port_name = re.search(r'Port\d+/\d+', line)
        if port_name:
            # We have found a line indicating some isis adjacency information
            port = Port(port_name[0].replace("Port", ""))
            adj = re.search(r'([\w-]+)', line.split()[-2])[0]
            status = re.search(r'(\w+)', line.split()[-1])[0]
            data.update({port: {"ISIS Adjacency": adj, "ISIS Status": status}})
    return data
