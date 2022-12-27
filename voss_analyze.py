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
from typing import Callable
import re
import csv

# This is a constant for identifying when a line is a line containing a command
COMMAND_IDENTIFIER = re.compile(r'Command:\[\d+\]')


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
        if COMMAND_IDENTIFIER.search(line):
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
                if cmd in line:
                    # One of the commands we are looking for has been found.
                    # We can now start gathering the output.
                    current_command = cmd
                    txt = []
        elif current_command:
            # We have found a command and are presently gathering output.
            txt.append(line)


def get_lldp_neighbors(text_lines: list[str]) -> dict[str, str]:
    """
    parse the output of "show lldp neighbor summary" and create a table correlating
    the port name and the lldp neighbor hostname

    :param text_lines: the output of "show lldp neighbor summary" seperated by lines
    :return: a dictionary holding lldp neighbor hostnames indexed by port names
    """
    # TODO: Parse the LLDP neighbor command output
    pass


# TODO: write parsing functions for ISIS adjacency, MAC table, and port state
def get_port_state(text_lines: list[str]) -> dict[str, str]:
    """
    parse the output of "show interfaces gigabitEthernet" and create a table correlating
    the port name and the port status

    :param text_lines: the output of "show interfaces gigabitEthernet" seperated by lines
    :return: a dictionary holding port states indexed by port names
    """
    data = {}
    pattern = re.compile(r'\d+\/\d+')
    for line in text_lines:
        match = text_lines.search(pattern)
        if match:
            status = re.search(r'up')
            data.update({port_name: {}})
    return data


# This is a dictionary mapping command text to a parsing function.
BINDINGS = {
    "show lldp neighbor summary": get_lldp_neighbors,
    "show interfaces gigabitEthernet": get_port_state
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
    # print(json.dumps(outputs, indent=2))

