#!/usr/bin/env python3
"""
A Network State Analysis Tool.
This will parse Extreme VOSS tech files for network state information including
ISIS Adjacencies, LLDP Neighbors, MAC Learning, and Port State. This script will then output
that information as a table in CSV format for use in Microsoft Excel. Exceptions are not
handled to provide a full stack trace in the event an exception does occur.
"""
import sys
import os
import argparse
from pathlib import Path
from typing import Any

# Set the path to the parent directory of the current file. Unless this script is
# moved, this should be the root of the project.
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
try:
    sys.path.index(path)
except ValueError:
    sys.path.append(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A Network State Analysis Tool")
    parser.add_argument("filename", type=Path, help="a filepath to a VOSS tech file")
    parser.add_argument("--output", "-o", type=Path, default=os.getcwd(), help="a filepath for the analysis output")
    args = parser.parse_args(sys.argv[1:])
    from base.switch import Port
    from voss import VOSS
    voss = VOSS.load(args.filename)
    # Search through the tech file for the commands we're looking for.
    # Pump the corresponding output through the bound parsing function.
    # Record the command and the parsed information in a dictionary.
    # outputs: dict[str, dict[Port, Any]] = {cmd: result for cmd, result in voss}
    # print(json.dumps(outputs, indent=2))
    # parsed_data = voss.parse()
    # print(json.dumps(parsed_data, indent=2))
    if not args.output.exists():
        args.output.mkdir()
    if args.output.is_dir():
        args.output = args.output / f"{args.filename.stem}.json"
    voss.save(args.output)

