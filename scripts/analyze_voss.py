#!/usr/bin/env python3
"""
A Network State Analysis Tool.
This will parse Extreme VOSS tech files for network state information including
ISIS Adjacencies, LLDP Neighbors, MAC Learning, and Port State. This script will then output
that information as a table in CSV format for use in Microsoft Excel. Exceptions are not
handled to provide a full stack trace in the event an exception does occur.
"""

import json
import sys
import os
import argparse
from pathlib import Path

from voss.voss import VOSS

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A Network State Analysis Tool")
    parser.add_argument("filename", type=Path, help="a filepath to a VOSS tech file")
    parser.add_argument("--output", "-o", type=Path, default=os.getcwd(), help="a filepath for the analysis output")
    args = parser.parse_args(sys.argv[1:])
    voss = VOSS.load(args.filename)
    # Search through the tech file for the commands we're looking for.
    # Pump the corresponding output through the bound parsing function.
    # Record the command and the parsed information in a dictionary.
    outputs = {cmd: result for cmd, result in voss}
    # TODO: Merge the parsed data around the primary key, the port name
    print(json.dumps(outputs, indent=2))
