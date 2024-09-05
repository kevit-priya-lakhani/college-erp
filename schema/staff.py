from marshmallow import Schema, fields, validate

class PlainStaffSchema(Schema):
    """Schema for staff data without timestamps."""
    _id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True, validate=validate.Regexp(".*@.*staff.*"))
    phone = fields.Int(required=True)
    dept = fields.Str(required=True)
    is_admin = fields.Bool(default=False)
    password = fields.Str(required=True, load_only=True)

class StaffSchema(PlainStaffSchema):
    """Schema for staff data including creation and update timestamps."""
    created_at = fields.Str(required=True)
    updated_at = fields.Str()

class StaffUpdateSchema(Schema):
    """Schema for updating staff information."""
    _id = fields.Str(dump_only=True)
    name = fields.Str()
    email = fields.Email(validate=validate.Regexp(".*@.*staff.*"))
    phone = fields.Int()
    dept = fields.Str()
    is_admin = fields.Bool()
    password = fields.Str(load_only=True)

class StaffLogin(Schema):
    """Schema for staff login credentials."""
    staff_id = fields.Str(load_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)
