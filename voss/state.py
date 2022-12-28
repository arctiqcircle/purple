import re

from dynex import Port
from voss import VOSS


@VOSS.parser("show interfaces gigabitEthernet")
def get_port_state(text_lines: list[str]) -> dict[Port, str]:
    """
    parse the output of "show interfaces gigabitEthernet" and create a table correlating
    the port name and the port status

    :param text_lines: the output of "show interfaces gigabitEthernet" seperated by lines
    :return: a dictionary holding port states indexed by port names
    """
    data = {}
    pattern = re.compile(r'\d+\/\d+')
    searching = False
    for line in text_lines:
        if "Port Name" in line:
            # We found the section we want.
            searching = True
        elif "Port Config" in line:
            # We reached the next section. Stop searching.
            searching = False
        if searching:
            match = pattern.search(line)
            if match:
                port_name = match[0]
                data.update({port_name: 'up' in line})
    return data