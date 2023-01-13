# DynEx: _Scripts_

Each script in this directory has its own arguments and options, but they do share some commonalities. All of these scripts can produce a report in the form of a Markdown file when the `-r` or `--report` flag is used. The data collected and the report are both written to the file or directory specified by the `-o` or `--output` argument. If no output file is specified, the outputs use a default name based on the input file name(s).

All scripts include a help menu that can be accessed by running the script with the `-h` or `--help` flag. In the help menu you will be able to find a description of the default output name, as well as a description of the arguments and options that are available for each script.

## VOSS Scripts

### *analyze_voss.py*
Analyzes a VOSS switch's tech file and outputs the switch's state. This state includes basic port information as well as information on ISIS, LLDP, MAC learning, and more. `analyze_voss.py` accepts a single tech file as a required positional argument. `analyze_voss.py` will output a raw `.json` file by default.

### *compare_voss.py*
Compares the state of two VOSS switches and outputs the differences between them. To use this script, you will need to have two tech files for the switches you want to compare. If there is an expectation that ports will change state between the two tech files, you can specify an optional file containing a mapping of ports between the two tech files using the `-m` or `--mapping` flag. This file should be in YAML or JSON format according to the following example:
```yaml
---
Interface:
  - from: 1/1
    to: 1/2
  - from: 1/2
    to: 1/1
```

where `from` is the port names in the first tech file and `to` is the port names in the second tech file. If the two tech files are from different switches, especially after a migration, this mapping file is a requirement for an accurate comparison.
