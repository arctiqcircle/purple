from __future__ import annotations

import re
import json
from pathlib import Path
from collections.abc import Collection, Iterable
from typing import Any, Type, Callable

from abc import ABC
from model.switch import Switch, SourceData


class TechFile(SourceData):
    """
    A TechFile object represents a VOSS tech file.

    It can be used to extract the output of commands.
    """

    @classmethod
    def extractor(cls, text: Iterable[str], command_set: Collection[str]) -> (str, list[str]):
        """
            parse the tech file for the output of a given command and yield the results

            :param text: the content of a VOSS tech file as an iterable of lines
            :param command_set: the commands to extract output of
            :return: a tuple holding the command and the command output
            """

        def _command_id(_c: str) -> re.Pattern:
            return re.compile(fr'Command:\[\d+\] \[\s*{_c}\s*\]')

        current_command = None
        txt = []
        for line in text:
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


class VOSS(Switch):
    """
    The VOSS Class is a subclass of the `Switch` class.

    This class implements the abstract methods of the Switch class for VOSS specific functionality.
    """

    def __init__(self, tech_file: TechFile):
        """
        Create a new VOSS object.

        :param tech_file: a TechFile object
        """
        self.tech_file = tech_file

    @classmethod
    def load(cls, tech_file_path: Path):
        """
        Load a TechFile from a Path and create a new VOSS object.

        :param tech_file_path: the path to the tech file
        :return: a VOSS object
        """
        return cls(TechFile.load(tech_file_path))

    def save(self, filename: str) -> None:
        """
        Save the data in the tech file to a JSON file.
        This requires the data to be parsed first and
        then translating the named tuples into
        strings so that they can be serialized.

        :param filename: the name of the new file
        """
        serialized = { t.__name__: { str(k): v for k, v in d.items() } for t, d in self }
        with open(filename, 'w') as f:
            json.dump(serialized, f, indent=2, default=lambda x: str(x))

    def __getitem__(self, t: Type[VOSS.Object]) -> dict[VOSS.Object, Any] | None:
        """
        Get the all the parsed results for a given VOSS.Object Type.

        :param t: the Type of the objects to return
        :return: a dictionary of the parsed results
        """
        for object_type, data in self:
            if t == object_type:
                return data
        return None

    def __iter__(self) -> tuple[Type[VOSS.Object], dict[VOSS.Object, Any]]:
        """
        Iterate over all the Types in the VOSS.Object class and yield all
        the parsed results for each Type.
        """
        # If we have iterated before we can yield from the data we have already parsed.
        if not self._data_store:
            tmp = {}
            # We need to parse all the results in the tech file in order to correlate all results of the same type and object.
            for command, result in self.tech_file:
                for network_object, data in result.items():
                    # We need to make sure that we have a dictionary for each type.
                    tmp[type(network_object)] = tmp.get(type(network_object), {})
                    # We need to make sure that we have a dictionary for each object.
                    tmp[type(network_object)][network_object] = tmp[type(network_object)].get(network_object, {})
                    # We now update the tmp dictionary with the new data.
                    # However, because the result of the parsing function is a dictionary
                    # of Any. We need to make sure the Any can be entered into the dictionary.
                    d = data if isinstance(data, dict) else { type(data).__name__: data }
                    tmp[type(network_object)][network_object].update(d)
            # Now that we have all the data, we can yield it through recursion.
            self._data_store = tmp
        for t, d in self._data_store.items():
            yield t, d

    def __contains__(self, t: Type[VOSS.Object]) -> bool:
        """
        Check if the tech file contains data for a given VOSS.Object Type.

        :param t: the Type of the objects to check for
        :return: True if the tech file contains data for the given Type, False otherwise
        """
        return self[t] is not None

    def read(self) -> dict[Type[VOSS.Object], dict[VOSS.Object, Any]]:
        """
        Read the tech file and return all the parsed results.

        :return: a dictionary of all the parsed results
        """
        return dict(self)