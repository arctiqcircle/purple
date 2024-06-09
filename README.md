# Purple

Arctiq Purple is an automation tool for working with Extreme Networks switching platforms including the EXOS and VOSS operating systems.

[![Version](https://img.shields.io/github/v/release/arctiqcircle/heatwave?sort=semver&logo=github&style=flat-square&label=Main%20Release)](https://github.com/arctiqcircle/blue/releases)

[![GNU GPL License](https://img.shields.io/badge/GNU_General_Purpose_License_v3-maroon.svg?logo=gnu&style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Getting Started

To get started with Purple, you will need to have Python 3 installed on your system. You can download Python 3 from [here](https://www.python.org/downloads/). It is required that you use Python version 3.10 or higher.

### Installation

To install Purple, you will need to clone the repository to your local machine. Once you have installed git, you can do this by running the following command in your terminal:

```bash
git clone https://github.com/arctiqcircle/purple.git
```

If you do not have git installed, you can download the repository as a zip file by clicking the green "Code" button on the top right of the repository page and selecting "Download ZIP".

In order to run the scripts located in the [scripts'](scripts) directory, you may need to make the scripts executable. To do this, you can run the following command in your terminal:

```bash
chmod +x scripts/*
```

To set permissions on a Windows machine you will need to access the properties of the file and check the "Allow executing file as program" box.

Finally, you will need to install the required Python packages. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

### Usage

To use Purple you will need to gather a collection of command outputs from the switch(s) you want to analyze.

Once you have the proper collection, you can run the scripts located in the [scripts](scripts) directory to analyze the switch(s). You can consult the documentation in that directory for more information on the operation of specific scripts.

Every script has a help menu that can be accessed by running the script with the `-h` or `--help` flag.
