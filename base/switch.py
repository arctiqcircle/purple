from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Collection, Iterable
from typing import Any, Callable, Type
from pathlib import Path

import json


class SourceData(ABC):
    """
    A SourceData is a dataclass that is used to represent a switch objects
    raw data. It is used to parse the raw data into a Switch Object.
    This class contains methods for parsing the output of commands which are
    injected into the class at runtime by the parser decorator.

    The SourceData can be iterated over to parse the output of each command.
    Using a `with` statement, the SourceData can be refreshed.

    Attributes:
        _data_stream: the raw data
        _commands: a dictionary of commands and their associated parsing methods
        _data_store: a dictionary of parsed data
    """

    _commands: dict[str, Callable] = {}
    _data_store: dict[str, dict[Switch.Object, Any]] = {}
    _data_stream: Iterable[str] = None

    @classmethod
    @abstractmethod
    def extractor(cls, text_lines: Iterable[str], command_set: Collection[str]) -> (str, list[str]): ...

    @classmethod
    def load(cls, tech_file_path: Path):
        """
        Load a tech file from a file path.
        To cut down on memory usage, the tech file is not loaded into memory
        at instantiation time. Instead, the tech file is loaded into memory
        by a `with` statement and read as needed line by line.

        :param tech_file_path: the path to the tech file
        :return: a VOSS object
        """

        # We overload the __enter__ method to open the file
        def open_tech_file(self):
            # When a tech file is opened, we want to
            # refresh the data store and data stream
            self._data_store = {}
            self._data_stream = open(tech_file_path, 'r')

        cls.__enter__ = lambda self: open_tech_file(self)
        # We overload the __exit__ method to close the file.
        # We don't clear the data store here because the user may want to continue to read.
        # Instead, we clear the data store when the tech file is opened.
        cls.__exit__ = lambda self, exc_type, exc_val, exc_tb: self._data_stream.close()
        return cls()

    def save(self, filename: Path):
        """
        Save the data in the `SourceData` to a JSON file
        representing the parsed output of each command.

        :param filename: the `Path` of the new file
        """
        with self:
            serialized = {cmd: obj for cmd, obj in self}
        with open(filename, 'w') as f:
            json.dump(serialized, f, indent=2)

    def __enter__(self):
        # This method is overloaded depending on where the tech file is loaded from.
        raise NotImplementedError('No __enter__ method has been defined for this SourceData.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        # This method is overloaded depending on where the tech file is loaded from.
        raise NotImplementedError('No __exit__ method has been defined for this SourceData.')

    def __getitem__(self, command: str) -> dict[Switch.Object, Any]:
        """
        Return the parsed output of a given command.

        :param command: the command to parse
        :return: the parsed results of the command
        """
        # If the command has already been parsed, return the results.
        # If it hasn't been parsed yet, iterate over the entire SourceData
        # as normal, but stop as soon as the command is encountered.
        if command in self._data_store:
            return self._data_store[command]
        # The iteration process will automatically populate the data store
        for cmd, obj in self:
            if cmd == command:
                return obj

    def __iter__(self) -> tuple[str, dict[Switch.Object, Any]]:
        """
        Iterate over the entire SourceData, parsing each command as it is encountered
        in the data stream. Use the extractor method to find the command and its
        associated output. Save the parsed output of each command to the data store.

        :return: a tuple containing the command and the parsed results
        """
        for cmd, lines in self.__class__.extractor(self._data_stream, self._commands.keys()):
            self._data_store[cmd] = self._commands[cmd](lines)
            yield cmd, self._data_store[cmd]

    def read(self) -> dict[str, dict[Switch.Object, Any]]:
        """
        Read the entire tech file into memory and return the parsed output of each command.

        :return: a dictionary containing the parsed output of each command
        """
        return {cmd: obj for cmd, obj in self}

    @classmethod
    def parser(cls, command: str) -> Callable:
        """
        This decorator is used to inject parsing functions into the class.
        The parsing function must take a list of strings as its only argument
        and return a dictionary.
        These functions are accessible via direct call, iteration, and item access.

        :param command: the command to bind the parsing function to
        :return: the parsing function
        """
        def _parser(func: Callable) -> Callable:
            setattr(cls, func.__name__, func)
            cls._commands[command] = func
            return func
        return _parser


class Switch(ABC):
    """
    The Switch class is a container for the state and functionality of any given switch.
    It is instantiated with a SourceData object which is used to parse the raw data into
    a Switch object.
    """

    class Object(ABC):
        """
        A Switch Object is a special dataclass for storing, comparing, and
        differentiating between different objects of the same type.
        """

        @abstractmethod
        def __eq__(self, other) -> bool:
            """
            compare two objects for equality and return a boolean
            """
            ...

        @abstractmethod
        def __ne__(self, other) -> dict | None:
            """
            compare two objects for inequality and return a dictionary of differences
            or return None if they are equal
            """
            ...

    @abstractmethod
    def __init__(self, source_data: SourceData): ...

    @classmethod
    @abstractmethod
    def load(cls, filename: str): ...

    @abstractmethod
    def save(self, filename: str) -> None: ...

    @abstractmethod
    def __getitem__(self, t: Type) -> dict[Switch.Object, Any]: ...

    @abstractmethod
    def __iter__(self) -> tuple[Type, dict[Switch.Object, Any]]: ...