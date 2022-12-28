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
    port_name = None
    for line in text_lines:
        if re.search(r'Port: *\d+/\d+', line):
            # We have found a line indicating the beginning of some LLDP neighbor information
            # Extract the local port name from this line and enter it in the data table
            port_name = re.search(r'\d+/\d+', line)[0]
            data.update({port_name: {}})
        elif "SysName" in line:
            # This line contains hostname (SysName) information
            # Grab the SysName. It is the last word on the line.
            data[port_name]["SysName"] = line.split()[-1].strip()
        elif "PortId" in line:
            # This line contains remote port information
            # Grab the port name. It is the last word in the line.
            data[port_name]["PortId"] = line.split()[-1].strip()
            pass
    return data
