import re
from pathlib import Path
from collections.abc import Collection
from typing import Any, NamedTuple
from dynex import Switch


class VOSS(Switch):
    """
    The VOSS Class is a subclass of the Switch class.
    This class implements the abstract methods of the Switch class for VOSS specific functionality.
    """

    def __init__(self, tech_lines: list[str]):
        """
        Create a new VOSS object.

        :param tech_lines: the content of the tech file seperated by lines.
        """
        self.tech_file = tech_lines

    @classmethod
    def load(cls, tech_file_path: Path):
        """
        Load a tech file and return a VOSS object.

        :param tech_file_path: the path to the tech file
        :return: a VOSS object
        """
        with open(tech_file_path, 'r') as f:
            return cls(f.readlines())

    def __getitem__(self, command: str) -> dict[NamedTuple, Any]:
        """
        Run the parsing function for a given command and return the result.
        This is less memory efficient than iteration over the VOSS object, but it is more convenient.

        :param command: the command to parse
        :return: the parsed results
        """
        _, lines = _extract_commands(self.tech_file, [command])
        return self._commands[command](lines)

    def __iter__(self) -> tuple[str, dict[NamedTuple, Any]]:
        """
        Iterate over the commands in the tech file and return the command and the parsed results.
        This is more memory efficient than direct call, but it is less convenient.

        :return: a tuple containing the command and the parsed results
        """
        for cmd, lines in _extract_commands(self.tech_file, self._commands.keys()):
            yield cmd, self._commands[cmd](lines)

    def parse(self) -> dict[NamedTuple, dict[str, Any]]:
        """
        Parse all the data in the tech file for which we have parsing functions.
        Group the results by the type of the indexing object into a new dictionary.
        All these new dictionaries are then added to a new dictionary where they're
        keyed by the name of the type of the indexing object.

        :return: combined parsed data
        """
        data = {}
        for cmd, result in self:
            for indexing_object, sub_data in result.items():
                t = type(indexing_object)
                if t not in data:
                    data[t] = {}
                if indexing_object not in data[t]:
                    data[t][indexing_object] = {}
                d = sub_data if isinstance(sub_data, dict) else {type(sub_data): sub_data}
                data[t][indexing_object].update(d)
        return data


def _extract_commands(text_lines: list[str], command_set: Collection[str]) -> (str, list[str]):
    """
    parse the tech file for the output of a given command and yield the results

    :param text_lines: the content of a VOSS tech file seperated by lines
    :param command_set: the commands to extract output of
    :return: a tuple holding the command and the command output
    """

    def _command_id(_c: str) -> re.Pattern:
        return re.compile(fr'Command:\[\d+\] \[\s*{_c}\s*\]')

    current_command = None
    txt = []
    for line in text_lines:
        if re.search(r"Command:\[\d+\]", line):
            # This line contains a command.
            if current_command:
                # We have reached a new command, and we have been gathering output.
                # This means we have finished gathering the output of the command.
                # So we yield the result.
                tmp = current_command, txt
                current_command = None
                txt = []
                yield tmp
            for cmd in command_set:
                if _command_id(cmd).search(line):
                    # One of the commands we are looking for has been found.
                    # We can now start gathering the output. We use the state of current_command to signal this.
                    current_command = cmd
                    txt = []
        elif current_command:
            # We have found a command and are presently gathering output.
            txt.append(line)
