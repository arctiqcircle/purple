#!/usr/bin/env python3
"""
A Network State Analysis Tool.
This script will parse Extreme VOSS tech files for network state information including
ISIS Adjacencies, LLDP Neighbors, MAC Learning, and Port State. This script will then output
that information as a table in CSV format for use in Microsoft Excel. Exceptions are not
handled to provide a full stack trace in the event an exception does occur.
"""
import json
import sys
import os
import argparse
from pathlib import Path
from typing import Callable, Tuple
import re
import csv


def command_id(_c: str) -> re.Pattern:
    return re.compile(fr'Command:\[\d+\] \[\s*{_c}\s*\]')


def extract_commands(text_lines: str, command_set: list[str]) -> (str, list[str]):
    """
    parse the tech file for the output of a given command

    :param text_lines: the content of a VOSS tech file seperated by lines
    :param command_set: the commands to extract output of
    :return: a tuple holding the command and the command output
    """
    current_command = None
    txt = []
    for line in text_lines:
        if re.search(r"Command:\[\d+\]", line):
            # This line contains a command.
            if current_command:
                # We have reached a new command, and we have been gathering output.
                # This means we have finished gathering the output of the command.
                # So we yield the result.
                tmp = current_command, txt
                current_command = None
                txt = []
                yield tmp
            for cmd in command_set:
                if command_id(cmd).search(line):
                    # One of the commands we are looking for has been found.
                    # We can now start gathering the output.
                    current_command = cmd
                    txt = []
        elif current_command:
            # We have found a command and are presently gathering output.
            txt.append(line)


def get_lldp_neighbors(text_lines: list[str]) -> dict[str, dict[str, str]]:
    """
    parse the output of "show lldp neighbor" and create structured data correlating
    the local port name with the lldp neighbor hostname and remote port name

    :param text_lines: the output of "show lldp neighbor summary" seperated by lines
    :return: a dictionary holding lldp neighbor hostnames and remote port indexed by port names
    """
    # TODO: Parse the LLDP neighbor command output
    data = {}
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


def get_port_state(text_lines: list[str]) -> dict[str, str]:
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

# TODO: write parsing functions for ISIS adjacency and MAC table


# This is a dictionary mapping command text to a parsing function.
BINDINGS: dict[str, Callable] = {
    "show lldp neighbor": get_lldp_neighbors,
    "show interfaces gigabitEthernet": get_port_state,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A Network State Analysis Tool")
    parser.add_argument("filename", type=Path, help="a filepath to a VOSS tech file")
    parser.add_argument("--output", "-o", type=Path, default=os.getcwd(), help="a filepath for the analysis output")
    args = parser.parse_args(sys.argv[1:])
    content = []
    with open(args.filename, 'r') as f:
        content = f.readlines()
    # Search through the tech file for the commands we're looking for.
    # Pump the corresponding output through the bound parsing function.
    # Record the command and the parsed information in a dictionary.
    outputs = {command: BINDINGS[command](output) for command, output in extract_commands(content, BINDINGS.keys())}
    # TODO: Merge the parsed data around the primary key, the port name
    print(json.dumps(outputs, indent=2))
