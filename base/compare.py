from pathlib import Path
import json
from yaml import FullLoader, load
import difflib

from base.typing import Switch

class Comparison:
    """
    The Comparison class is used to compare the data in two VOSS objects.
    You can optionally specify a mapping of keys between the two objects.
    This will allow you to compare data that is keyed by different objects.
    This is useful for comparing before and after data.

    This object is serializable to JSON and can be used to generate a report.
    """
    def __init__(self, mapping: dict[str, str]):
        """
        Create a new Comparison object.

        :param mapping: a mapping of keys between the two objects
        """
        self.mapping = mapping

    @classmethod
    def load(cls, mapping_file_path: Path):
        """
        Load a mapping file and return a Comparison object.
        The mapping file can be a JSON or YAML file.
        It should be a dictionary of type keys to a sub-dictionary of before keys to after keys.

        :param mapping_file_path: the path to the mapping file
        :return: a Comparison object
        """
        with open(mapping_file_path, 'r') as f:
            if mapping_file_path.suffix == '.json':
                mapping = json.load(f)
            elif mapping_file_path.suffix in ('.yaml', '.yml'):
                mapping = load(f, Loader=FullLoader)
            else:
                raise ValueError('The mapping file must be a JSON or YAML file.')
        return cls(mapping)

    def __call__(self, before: Switch, after: Switch) -> dict[str, dict[str, dict[str, str]]]:
        """
        Compare the data in two Switch objects. If the two Switch objects are not of the same type,
        then the comparison will fail with a TypeError.

        This method uses the .parse() method of the Switch object to get the data.
        The mapping is then used to convert the keys of the before object to the keys of the after object
        allowing the comparison to be made directly.

        :param before: the before object
        :param after: the after object
        :return: a dictionary of differences
        """
        # TODO: Add support for comparing different types of Switch objects
        raise NotImplementedError('This method has not been implemented yet.')

