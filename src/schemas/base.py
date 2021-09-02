import datetime as dt
import marshmallow as ma


class RzFieldDateTime(ma.fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, dt.datetime):
            raise ma.ValidationError("Value must be a datetime object")
        return int(value.timestamp())

    # def _deserialize(self, value, attr, data, **kwargs):
    #     try:
    #         return [int(c) for c in value]
    #     except ValueError as error:
    #         raise ma.ValidationError("Pin codes must contain only digits.") from error
