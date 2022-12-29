import re
from typing import Any

from dynex import Interface, Network
from voss import VOSS


@VOSS.parser("show ip interface")
def get_ip_interfaces(text_lines: list[str]) -> dict[Interface, Network]:
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
                yield Interface(interface_name), Network(matches[0], matches[1])
    return {iface: net for iface, net in search_lines()}


@VOSS.parser("show ip route")
def get_ip_routes(text_lines: list[str]) -> dict[Network, dict[str, Any]]:
    """
    parse the output of "show ip route" and create structured data correlating
    the network address and subnet mask with the next hop and outgoing interface

    :param text_lines: the output of "show ip route" seperated by lines
    :return: a dictionary holding next hop and outgoing interface indexed by network address and subnet mask
    """
    def search_lines() -> tuple[Network, dict[str, Any]]:
        for line in text_lines:
            # Check if this line contains IP address information by searching for a valid IP address pattern.
            matches = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            if matches:
                # We have found a line containing IP address information.
                # The first match is the destination IP address, the second is the subnet mask.
                # There may or may not be a third match, because the next hop may not be an IP address.
                network = Network(matches[0], matches[1])
                hop = matches[2] if len(matches) == 3 else line.split()[2].strip()
                iface = line.split()[5].strip()
                iface = Interface(iface) if re.search(r'[a-zA-Z]]', iface) else Interface("Vlan" + iface)
                yield network, {"next_hop": hop, "outgoing_interface": iface}
    return {net: data for net, data in search_lines()}
