# DynEx: _Scripts_

Each script in this directory has its own arguments and options, but they do share some commonalities. All of these scripts produce a report in the form of a Markdown file. The report is written to the file specified by the `-o` or `--output` argument. If no output file is specified, the report uses a default name based on the input file name(s). All scripts include a help menu that can be accessed by running the script with the `-h` or `--help` flag. In the help menu you will be able to find a description of the default report name, as well as a description of the arguments and options that are available for each script.

## VOSS Scripts

### *analyze_voss.py*
Analyzes a VOSS switch's tech file and outputs a report of the switch's state. This report includes basic port information as well as information on ISIS, LLDP, and MAC learning. `analyze_voss.py` accepts a single tech file as a required positional argument. Along with a report file, `analyze_voss.py` will also output a `.json` file containing the raw data used to generate the report.

### *compare_voss.py*
Compares the state of two VOSS switches and outputs a report of the differences between them. To use this script, you will need to have two tech files for the switches you want to compare. If there is an expectation that ports will change state between the two tech files, you can specify an optional file containing a mapping of ports between the two tech files using the `-m` or `--mapping` flag. This file should be a CSV file with the following format:

```shell
first,second
1/1,1/2
1/2,1/3
```

where `first` is the port names in the first tech file and `second` is the port names in the second tech file. If the two tech files are from different switches, this mapping file is a requirement for an accurate report.
