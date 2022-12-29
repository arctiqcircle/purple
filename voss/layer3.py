import re
from typing import Any

from dynex import Interface
from voss import VOSS


@VOSS.parser("show ip interface")
def get_ip_interfaces(text_lines: list[str]) -> dict[Interface, dict[str, str]]:
    """
    parse the output of "show ip interface" and create structured data correlating
    the local interface name with the ip address and subnet mask

    :param text_lines: the output of "show ip interface" seperated by lines
    :return: a dictionary holding ip address and subnet mask indexed by interface names
    """
    def search_lines() -> tuple[Interface, dict[str, str]]:
        for line in text_lines:
            # Check if this line contains IP address information by searching for a valid IP address pattern.
            matches = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            if matches:
                # We have found a line containing IP address information.
                # The first match is the IP address, the second is the subnet mask.
                # The interface name is the first word on the line.
                interface_name = line.split()[0]
                yield Interface(interface_name), {"IP Address": matches[0], "Subnet Mask": matches[1]}
    return {iface: data for iface, data in search_lines()}


@VOSS.parser("show ip route")
def get_ip_routes(text_lines: list[str]) -> dict[Interface, dict[str, Any]]:
    """
    parse the output of "show ip route" and create structured data correlating
    an interface with a destination IP address and subnet mask and the next hop IP address

    :param text_lines: the output of "show ip route" seperated by lines
    :return: a dictionary with destination IP address, mask, next hop indexed by interface names
    """
    def search_lines() -> tuple[Interface, dict[str, Any]]:
        for line in text_lines:
            # Check if this line contains IP address information by searching for a valid IP address pattern.
            matches = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            if matches:
                # We have found a line containing IP address information.
                # The first match is the destination IP address, the second is the subnet mask.
                # There may or may not be a third match, because the next hop may not be an IP address.
                pass

    pass
