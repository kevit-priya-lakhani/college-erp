from marshmallow import Schema, fields, validate
from enum import Enum
# from marshmallow_enum import EnumField

class LoginSchema(Schema):
    """Schema for user login credentials."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)
