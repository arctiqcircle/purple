from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod

from base.switch import Switch


@dataclass(frozen=True)
class Port(Switch.Object):
    """
    A Port is a layer 2 construct that is used to connect two devices together.
    It has a defined up or down state. It can learn MAC addresses which are out
    the port. It can form peering with new ports via a variety of protocols.
    """
    name: str

    def __eq__(self, new: Port) -> bool:
        return self.name == new.name

    def __ne__(self, new: Port) -> dict | None:
        if self.name != new.name:
            return {"old": self.name, "new": new.name}
        return None


@dataclass(frozen=True)
class Interface(Switch.Object):
    """
    An Interface is a layer 3 construct that is used to identify a device on a network.
    It can correspond to a physical port on a device, or it can be a logical construct.
    """
    name: str

    def __eq__(self, new: Interface) -> bool:
        return self.name == new.name

    def __ne__(self, new: Interface) -> dict | None:
        if self.name != new.name:
            return {"old": self.name, "new": new.name}
        return None

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
