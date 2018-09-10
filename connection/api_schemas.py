"""
Set up marshmallow classes for serialising data
"""
# pylint: disable=I0011, W0613

from marshmallow import validates_schema
from webargs.fields import Int, Nested, Str
from werkzeug.exceptions import BadRequestKeyError

from .constants import JobStatus
from .schemas import ma


class JobArgs(ma.Schema):
    """
    Class to read in arguments to create a new job
    """

    class Meta:
        """
        Ensure that it can only take the defined arguments
        """

        strict = True

    case_id = Int(required=True)
    author = Str(required=True)
    name = Str(required=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        """
        Ensure no additional fields are passed
        """
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise BadRequestKeyError("Unknown field", unknown)


class JobArgumentArgs(ma.Schema):
    """
    Class to read in the arguments for a single Job argument value
    """

    class Meta:
        """
        Ensure that other fields are not provided
        """

        strict = True

    name = Str(required=True)
    value = Str(required=True)

    @validates_schema(pass_original=True, pass_many=True)
    def check_unknown_fields(self, data, original_data, many):
        """
        Ensure no additional fields are passed
        """
        if not many:
            self.check_unknown_field(data, original_data)
            return
        if len(data) != len(original_data):
            raise BadRequestKeyError(
                "Could not parse all fields, {}".format(original_data)
            )
        for index in range(0, len(data)):
            self.check_unknown_field(data[index], original_data[index])

    def check_unknown_field(self, data, original_data):
        """
        Check that a single instance of a field validates
        """
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise BadRequestKeyError("Unknown field {}".format(unknown))


class JobPatchArgs(ma.Schema):
    """
    Read in the arguments for patching a job
    """

    class Meta:
        """
        Ensure that other fields are not provided
        """

        strict = True

    name = Str()
    description = Str()
    values = Nested(JobArgumentArgs, many=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        """
        Ensure no additional fields are passed
        """
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise BadRequestKeyError("Unknown field {}".format(unknown))


class PaginationArgs(ma.Schema):
    """
    Read in arguments for paginating
    """

    class Meta:
        """
        Ensure that other fields are not provided
        """

        strict = True

    page = Int(missing=1, strict=True, validate=lambda p: p > 0)
    per_page = Int(missing=10, strict=True, validate=lambda p: p > 0)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        """
        Ensure no additional fields are passed
        """
        unknown = set(original_data) - set(self.fields)
        if len(unknown) > 0:
            raise BadRequestKeyError("Unknown field {}".format(unknown))


class SearchArgs(ma.Schema):
    """
    Read in arguments for searching
    """

    class Meta:
        """
        Ensure that other fields are not provided
        """

        strict = True

    name = Str(missing=None, strict=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        """
        Ensure no additional fields are passed
        """
        unknown = set(original_data) - set(self.fields)
        if len(unknown) > 0:
            raise BadRequestKeyError("Unknown field {}".format(unknown))


class StatusPatchSchema(ma.Schema):
    """
    Read in arguments for setting a status value
    """

    class Meta:
        """
        Ensure that other fields are not provided
        """

        strict = True

    status = Str(validate=lambda s: s.upper() in JobStatus.__members__.keys())

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        """
        Ensure no additional fields are passed
        """
        unknown = set(original_data) - set(self.fields)
        if len(unknown) > 0:
            raise BadRequestKeyError("Unknown field {}".format(unknown))


class OutputArgs(ma.Schema):
    """
    Check read-in arguments for creating a job Output.
    """

    class Meta:
        """
        Ensure that it can only take the defined arguments
        """

        strict = True

    destination = Str(required=True)
    type = Str(required=True)
    name = Str(required=True)
    label = Str(required=True)
    filename = Str(required=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        """
        Ensure no additional fields are passed
        """
        unknown = set()
        for output in original_data:
            unknown = set(unknown).union(set(output)) - set(data)
        if unknown:
            raise BadRequestKeyError("Unknown field", unknown)


class OutputListArgs(ma.Schema):
    """
    List of job outputs
    """

    class Meta:
        """
        Ensure that other fields are not provided
        """

        strict = True

    outputs = Nested(OutputArgs, many=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        """
        Ensure no additional fields are passed
        """
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise BadRequestKeyError("Unknown field {}".format(unknown))
