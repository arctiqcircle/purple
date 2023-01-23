from __future__ import annotations
from dataclasses import dataclass

from base.switch import Switch


@dataclass(frozen=True)
class Basic(Switch.Object):
    """
    The Basic class is used to represent a basic object. This
    is any object that can be described in a single attribute.
    """
    name: str

    def __eq__(self, new: Connection) -> bool:
        return self.name == new.name

    def __ne__(self, new: Connection) -> dict | None:
        if self.name != new.name:
            return {"old": self.name, "new": new.name}
        return None

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class State(Basic):
    """
    The State class represents the operational or administrative state of a Switch object.
    """

@dataclass(frozen=True)
class Connection(Basic):
    """
    A Connection is an L2 or L3 connection between two systems.
    A Connection describes the other end of the connection.
    """

@dataclass(frozen=True)
class Interface(Basic):
    """
    An Interface is a layer 3 construct that is used to identify a device on a network.
    It can correspond to a physical port on a device, or it can be a logical construct.
    """

@dataclass(frozen=True)
class Network(Switch.Object):
    """
    A Network is a layer 3 construct denoting a range of consecutive IP addresses that
    are grouped by masks for routing purposes.
    """
    address: str
    mask: str

    def __eq__(self, new: Network) -> bool:
        return self.address == new.address and self.mask == new.mask

    def __ne__(self, new: Network) -> dict | None:
        if self.address != new.address or self.mask != new.mask:
            return {"old": f"{self.address}//{self.mask}", "new": f"{new.address}//{new.mask}"}
        return None

    def __str__(self) -> str:
        return f"{self.address}//{self.mask}"


@dataclass(frozen=True)
class Vlan(Switch.Object):
    """
    A Vlan is a layer 2 construct that is used to group ports together.
    """

    id: int
    name: str

    def __eq__(self, new: Vlan) -> bool:
        return self.id == new.id and self.name == new.name

    def __ne__(self, new: Vlan) -> dict[str, str] | None:
        if self.id != new.id or self.name != new.name:
            return {"old": f"VLAN({self.id}, {self.name})", "new": f"VLAN({new.id}, {new.name})"}
        return None


@dataclass(frozen=True)
class MacAddresses(Switch.Object):
    """
    A MacAddresses are a layer 2 construct that is used to identify a devices
    on an Ethernet network. They are learned by ports and are used to form
    tables for forwarding packets.
    """
    addresses: list[str]

    def __eq__(self, other: MacAddresses) -> bool:
        return self.addresses == other.addresses

    def __ne__(self, other) -> dict[str, list[str]] | None:
        if self == other:
            return None
        missing = [address for address in self.addresses if address not in other.addresses]
        gained = [address for address in other.addresses if address not in self.addresses]
        return {'missing': missing, 'gained': gained} if missing or gained else None

    def __str__(self) -> str:
        return ", ".join(self.addresses)
