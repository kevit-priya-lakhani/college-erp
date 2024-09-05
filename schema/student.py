
from marshmallow import Schema, fields, validate
from enum import Enum
# from marshmallow_enum import EnumField

class PlainStudentSchema(Schema):
    """Schema for student data without timestamps."""
    _id = fields.Str(dump_only=True)
    email = fields.Email(required=True, validate=validate.Regexp(".*@.*student.*"))
    name = fields.Str(required=True)
    phone = fields.Int(required=True)
    dept = fields.Str(required=True)
    batch = fields.Int(required=True)
    sem = fields.Int(required=True)
    password = fields.Str(required=True, load_only=True)

class StudentSchema(PlainStudentSchema):
    """Schema for student data including creation and update timestamps."""
    created_at = fields.Str(required=True)
    updated_at = fields.Str()

class StudentUpdateSchema(Schema):
    """Schema for updating student information."""
    email = fields.Email(validate=validate.Regexp(".*@.*student.*"))
    name = fields.Str()
    phone = fields.Int()
    dept = fields.Str()
    batch = fields.Int()
    sem = fields.Int()
    password = fields.Str()