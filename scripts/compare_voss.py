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
from datetime import datetime

# Set the path to the parent directory of the current file. Unless this script is
# moved, this should be the root of the project.
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
try:
    sys.path.index(path)
except ValueError:
    sys.path.append(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare the state of two VOSS tech files")
    parser.add_argument("initial_file", type=Path, help="a filepath to a initial VOSS tech file")
    parser.add_argument("latter_file", type=Path, help="a filepath to a latter VOSS tech file")
    parser.add_argument("--mapping", "-m", type=Path, default=None, help="a filepath to a mapping file")
    parser.add_argument("--output", "-o", type=Path, default=os.getcwd(), help="a filepath for the analysis output")
    args = parser.parse_args(sys.argv[1:])
    from base.compare import Comparison
    from voss import VOSS
    # We load the two tech files into two VOSS objects
    voss_old = VOSS.load(args.initial_file)
    voss_new = VOSS.load(args.latter_file)
    # We then compare the two objects using the Comparison class with the optional mapping file
    compare = Comparison.load(voss_old, voss_new, mapping_file_path=args.mapping)
    # We then output the results to a JSON file
    default_filename = f'{datetime.now().strftime("%m%d%-y-%H%M")}_compare.json'
    if not args.output.exists():
        compare.save(args.output)
    else:
        if args.output.is_dir():
            compare.save(args.output / default_filename)
        else:
            compare.save(args.output)
