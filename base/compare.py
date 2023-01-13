from __future__ import annotations

from collections.abc import Container, Iterable
from typing import Type, Any, Generic, TypeVar
from dataclasses import dataclass
from pathlib import Path

import json
from yaml import FullLoader, load

from base.switch import Switch

P = TypeVar('P', bound=Switch.Object.__subclasses__())

class MappingError(Exception):
    """
    A MappingError is raised when a component from a map is not found in the switch object.
    """

class Comparison:
    """
    The Comparison class is used to compare the data in two Switch objects.
    You can optionally provide a mapping of keys between the two objects
    which will be used to assert equality between the data when keys
    are not the same.

    This object is serializable to JSON and can be used to generate a report.
    """

    @dataclass
    class Pair(Generic[P]):
        old: P
        new: P

        def __eq__(self, other: Switch.Object) -> bool:
            return self.old == other

    def __init__(self, old: Switch, new: Switch, mapping: dict[Type, list[Pair]] = None):
        """
        Create a new Comparison object for comparing two Switch objects.

        :param old: the old object
        :param new: the new object
        :param mapping: a mapping by type of the keys between the two objects
        """
        self.mapping = mapping if mapping else {}
        self.old = old
        self.new = new

    @classmethod
    def load(cls, *args, mapping_file_path: Path):
        """
        Load a mapping file and return a Comparison object.
        The mapping file can be a JSON or YAML file.
        It should be a dictionary of type keys to a sub-dictionary of old keys to new keys.

        :param mapping_file_path: the path to the mapping file
        :return: a Comparison object
        """
        m = None
        if mapping_file_path:
            with open(mapping_file_path, 'r') as f:
                if mapping_file_path.suffix == '.json':
                    mapping = json.load(f)
                elif mapping_file_path.suffix in ('.yaml', '.yml'):
                    mapping = load(f, Loader=FullLoader)
                else:
                    raise ValueError('The mapping file must be a JSON or YAML file.')
            # We now have a dictionary of strings to a list of dictionaries of strings to strings. We need to convert the
            # root keys strings to BaseTypes and the values strings to Pairs of those type instances.
            # We use the subclasses of Switch.Object as the keys because we want to be able to use the subclasses
            # as the keys in the Pairs.
            subclasses = {t.__name__: t for t in Switch.Object.__subclasses__()}
            m = {
                subclasses[type_name]:
                    [Comparison.Pair(
                        subclasses[type_name](pair['before']),
                        subclasses[type_name](pair['after'])
                    ) for pair in pairs]
                for type_name, pairs in mapping.items()
            }
        return cls(*args, mapping=m)

    def save(self, file_path: Path):
        """
        Save the Comparison object to a JSON file.

        :param file_path: the path to the file
        """
        serialized = {t.__name__: {str(k): v for k, v in d.items() if v} for t, d in self}
        with open(file_path, 'w') as f:
            json.dump(serialized, f, default=lambda o: str(o), indent=2)

    def __getitem__(self, item: Type[Switch.Object]) -> dict[Switch.Object, Any]:
        """
        Get the differences for a given Type.

        :param item: the Type
        :return: a dictionary of differences by object of that Type
        """
        return dict(self)[item]

    def __iter__(self) -> tuple[Type[Switch.Object], dict[Switch.Object, Any]]:
        """
        Iterate over all the Types in the older Switch object and yield all
        the differences for each Type's object that actually has a difference.

        :return: a tuple of the Type and a dictionary of the differences by object of that Type
        """
        for t, old_data in self.old:
            if t not in self.new:
                raise ValueError(f'The new object does not have a {t.__name__} Type.')
            new_data = self.new[t]
            # We now have the old and new data for a given Type.
            # We need to compare the values of the objects in new and old.
            mapping = self.mapping.get(t, [])
            tmp = {}
            for old_object, old_values in old_data.items():
                # Now we need to find corresponding new values for the old values.
                if old_object not in mapping:
                    # We don't have a mapping for this object, so we assume the keying objects are the same for now.
                    new_object = old_object
                else:
                    # We have a mapping for this object. We need to find the new object that matches the mapping.
                    new_object = next(pair.new for pair in mapping if pair.old == old_object)
                    # If no new object matches the mapping, we throw a MappingError.
                    if new_object is None:
                        raise MappingError(f'The new {t.__name__} data has no object with the key {mapping[old_object].new}.')
                # If the object is not in the new data this could be for a number of reasons, but we will assume
                # that it is because the two switches have different objects of this type. That isn't an error, we
                # just don't want to compare it.
                if new_object not in new_data:
                    continue
                new_values = new_data[new_object]
                # We now have two corresponding old and new values for this object.
                # We need to compare them using a comparison generator capable of recursion.
                differences = { field: diff for field, diff in Comparison.compare(old_values, new_values) if diff }
                differences.update({ "old": old_object } if differences else {})
                tmp[new_object] = differences
            # We now have a dictionary of differences for this Type.
            yield t, tmp

    @staticmethod
    def compare(old_values: dict[str, Switch.Object], new_values: dict[str, Switch.Object]) -> tuple[str, dict[str, Any]]:
        """
        Compare two arbitrary value dictionaries and yield the difference if there is one.

        :param old_values: the old values in a dictionary
        :param new_values: the new values in a dictionary
        :return: a tuple of the field_name and a dictionary describing the difference if there is one
        """
        for old_field_name, old_field_value in old_values.items():
            if old_field_name not in new_values:
                # Field exists in old but not new.
                yield old_field_name, {"old": old_field_value, "new": None}
                continue
            for new_field_name, new_field_value in new_values.items():
                if new_field_name not in old_values:
                    # Field exists in new but not in old.
                    yield new_field_name, {"old": None, "new": new_field_value}
                    continue
                if old_field_name == new_field_name:
                    # Field exists in both old and new, compare values.
                    if type(old_field_value) != type(new_field_value):
                        raise TypeError(f'Field {old_field_name} has different types in old and new.')
                    if isinstance(old_field_value, dict):
                        # If the value is another dictionary, we need to recurse.
                        new_field_value: dict
                        yield old_field_name, { k: v for k, v in Comparison.compare(old_field_value, new_field_value) }
                    diff = old_field_value != new_field_value
                    if diff:
                        # Finally, if the values are different, yield the difference.
                        yield old_field_name, diff
                    # If the two are the same, we don't need to do anything. We just move on to the next field.





