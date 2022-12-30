# Sample Tech Files

This directory contains sample tech files for testing purposes.
These files are set up to mock some kind of real-world scenario.
However, all of these files contain no sensitive information.
Inspection will reveal that many of the values are nonsensical, but this is intentional.

## VOSS Tech Files

Included in this directory are two VOSS tech files and a corresponding
mapping file. The mapping file is used to map the mock changes in the
first tech file to the second tech file. The following is a description
of the files and the mock changes that were made.

### _VOSS_CORE-1_MOCK(1).tech_
The `VOSS_CORE-1_MOCK(1).tech` file is a mockup of a VOSS tech file.
It describes a core device with nine (9) ports with four (4) active connections.
All four (4) connections have ISIS and LLDP with other mock devices, though
two (2) of the connections are to the same device. The following table shows
the mock connections.

| Port | Connected To       | Status |
|------|--------------------|--------|
| 1    | VOSS_CORE-2_MOCK   | Up     |
| 2    | VOSS_CORE-2_MOCK   | Up     |
| 3    |                    | Down   |
| 4    |                    | Down   |
| 5    |                    | Down   |
| 6    |                    | Down   |
| 7    |                    | Down   |
| 8    | VOSS_DISTRO-1_MOCK | Up     |
| 9    | VOSS_DISTRO-2_MOCK | Up     |

Each "Up" port has learned three (3) unique MAC addresses.

### _VOSS_CORE-2_MOCK(2).tech_

The `VOSS_CORE-2_MOCK(2).tech` file is a mockup of a VOSS tech file showing
the aftermath of some mistaken changes made to the "VOSS_CORE-1_MOCK" VOSS switch.
It describes a core device with nine (9) ports with three (4) active connections.
Three (3) connections have ISIS and/or LLDP with other mock devices.
The following table shows the mock connections and whether they should be detected as mistakes.

| Port | Connected To       | Status | Mistake |
|------|--------------------|--------|---------|
| 1    | VOSS_CORE-2_MOCK   | Down   | Yes     |
| 2    | VOSS_CORE-2_MOCK   | Up     | No      |
| 3    | SERVER-1_MOCK      | Up     | No      |
| 4    |                    | Down   | No      |
| 5    | VOSS_BAD_SWITCH    | Up     | Yes     |
| 6    | VOSS_DISTRO-1_MOCK | Up     | No      |
| 7    |                    | Down   | No      |
| 8    |                    | Down   | No      |
| 9    |                    | Down   | No      |

Port 2 has learned all of Port 1's old MACs. Port 3 has learned new MAC addresses.
Port 5 has learned new MACs addresses. Port 6 has the same MACs as Port 8 from before.
The old Port 9's MACs are missing.

### _voss_core_mapping.yaml_

The `voss_core_mapping.yaml` file is a mapping file used to map the changes
intended to be made between the two VOSS tech files. The mapping file sets
expectations for what should be seen in the second tech file.

Specifically, the mapping file expects the following changes to have been made:
- No Changes for Port 1 or Port 2
  - Instead, Port 1 went down
- Port 3 received a new connection to SERVER-1_MOCK
- Port 8 should have migrated to Port 6
- Port 9 should have migrated to Port 7
  - Instead, some new cable was plugged into Port 5 and VOSS_DISTRO-2_MOCK was lost