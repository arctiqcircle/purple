#!/usr/bin/env python3
"""
A Network State Analysis Tool.
This will parse Extreme VOSS tech files for network state information.
"""
import sys
import os
import json
import argparse
from pathlib import Path

# Set the path to the parent directory of the current file. Unless this script is
# moved, this should be the root of the project.
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
try:
    sys.path.index(path)
except ValueError:
    sys.path.append(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare the state of two VOSS tech files")
    parser.add_argument("filename1", type=Path, help="a filepath to a VOSS tech file")
    parser.add_argument("filename2", type=Path, help="a filepath to a VOSS tech file")
    parser.add_argument("--mapping", "-m", type=Path, default=None, help="a filepath to a mapping file")
    parser.add_argument("--output", "-o", type=Path, default=os.getcwd(), help="a filepath for the analysis output")
    args = parser.parse_args(sys.argv[1:])
    from base.compare import Comparison
    from voss import VOSS
    # We load the two tech files into two VOSS objects
    voss1 = VOSS.load(args.filename1)
    voss2 = VOSS.load(args.filename2)
    # We then compare the two objects using the Comparison class with the optional mapping file
    compare = Comparison.load(args.mapping)
    delta = compare(voss1, voss2)
    # We then output the results to a JSON file
    if not args.output.exists():
        args.output.mkdir()
    with open(args.output / "delta.json", "w") as f:
        json.dump(delta, f, indent=2)
