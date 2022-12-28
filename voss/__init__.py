"""
The VOSS Package contains functions and classes for evaluating the state of Extreme VOSS Switches.
Each included module contains functions for parsing the output of a given command and returning structured data.
"""

# TODO: Add support for parsing ISIS adjacency and MAC table, include import
from voss.voss import VOSS
import voss.state
import voss.lldp
