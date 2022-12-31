# DynEx

> A collection of Python automation scripts for analyzing Extreme Networks VOSS and EXOS switches.
> These scripts parse the output of "show tech" commands and provide an analysis of the switches state.
> DynEx can then be used to compare the state of multiple switches and identify differences.

## Getting Started
To get started with DynEx, you will need to have Python 3 installed on your system.
You can download Python 3 from [here](https://www.python.org/downloads/).
It is required that you use Python version 3.10 or higher.

### Installation
To install DynEx, you will need to clone the repository to your local machine.
Once you have installed git, you can do this by running the following command in your terminal:

```bash
git clone https://github.com/dyntek-services-inc/dynex.git
```

If you do not have git installed, you can download the repository as a zip file by clicking the green "Code" button on the top right of the repository page and selecting "Download ZIP".

In order to run the scripts located in the [scripts'](scripts) directory, you may need to make the scripts executable.
To do this, you can run the following command in your terminal:

```bash
chmod +x scripts/*
```

To set permissions on a Windows machine you will need to access the properties of the file and check the "Allow executing file as program" box.

### Usage
To use DynEx, you will need to have a "tech file" for the switch(s) you want to analyze.
These tech files can be obtained by running the `show tech` command on the switch.

Once you have a tech file, you can run the scripts located in the [scripts'](scripts) directory to analyze the switch(s).
You can consult the documentation in that directory for more information on the operation of specific scripts.

Every script has a help menu that can be accessed by running the script with the `-h` or `--help` flag.
