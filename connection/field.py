"""
This module has helper classes and methods to deal
with fields and their validation
"""


class Field:
    """
    A class to represents fields in cases
    and do logical processing and validation
    with them
    """

    def __init__(self, name, properties={}):
        self.display_name = name
        self.process_name = name
        self.properties = properties
        self._validate()

    def set_properties(self, **properties):
        """
        Set a given set of properties
        """
        self.properties.update(properties)
        self._validate()

    def _validate(self):
        """
        Ensure that the internal state is valid
        """
        self.process_name = self.display_name
        label = self.properties.get('label')
        if label is not None:
            self.process_name = label
        prefix = self.properties.get('prefix')
        suffix = self.properties.get('suffix')
        if prefix is not None:
            self.process_name = prefix + self.process_name
        if suffix is not None:
            self.process_name = self.process_name + suffix

    def validate_value(self, fullname, new_value):
        """
        Check to make sure the current value is allowed.

        The current implementation only handles floats
        and the fields
        * min
        * max
        """
        new_value = float(new_value)
        if fullname != self.process_name:
            return False
        min = self.properties.get('min')
        if min is not None and float(min) > new_value:
            return False
        max = self.properties.get('max')
        if max is not None and float(max) < new_value:
            return False
        return True
