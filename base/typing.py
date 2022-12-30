from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Any, Callable, NamedTuple, Type

Port = namedtuple("Port", ['name'])
Port.__doc__ = """
A Port is a layer 2 construct that is used to connect two devices together.
"""
Interface = namedtuple("Interface", ['name'])
Interface.__doc__ = """
An Interface is a layer 3 construct that is used to identify a device on a network.
It can correspond to a physical port on a device, or it can be a logical construct.
"""
Network = namedtuple("Network", ['address', 'mask'])
Network.__doc__ = """
A Network is a layer 3 construct denoting a range of consecutive IP addresses that
are grouped by masks for routing purposes.
"""


class Switch(ABC):
    """
    The Switch class is a container for the state and functionality of any given switch.
    This class contains methods for parsing the output of commands which are injected into the class
    at runtime by the parser decorator.

    The data returned by the parser functions are accessed via direct call, iteration, and item access.
    """

    # This is a dictionary mapping command text to a parsing function.
    # It is populated by the parser decorator.
    _commands: dict[str, Callable] = {}

    @classmethod
    @abstractmethod
    def load(cls, filename: str): ...

    @abstractmethod
    def save(self, filename: str) -> None: ...

    @abstractmethod
    def __getitem__(self, command: str) -> dict[NamedTuple, Any]: ...

    @abstractmethod
    def __iter__(self) -> tuple[str, dict[NamedTuple, Any]]: ...

    @abstractmethod
    def parse(self) -> dict[Type, dict[NamedTuple, dict[str, Any]]]: ...

    @classmethod
    def parser(cls, command: str) -> Callable:
        """
        This decorator is used to inject parsing functions into the class.
        The parsing function must take a list of strings as its only argument and return a dictionary keyed by Port.
        These functions are accessible via direct call, iteration, and item access.

        :param command: the command to bind the parsing function to
        :return: the parsing function
        """

        def _parser(func: Callable) -> Callable:
            setattr(cls, func.__name__, func)
            cls._commands[command] = func
            return func
        return _parser