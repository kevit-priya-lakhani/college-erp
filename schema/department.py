from marshmallow import Schema, fields, validate

class DepartmentSchema(Schema):
    """Schema for department records."""
    _id = fields.Str(load_only=True)
    name = fields.Str(required=True, unique=True)
    created_at = fields.Str()
    updated_at = fields.Str()
