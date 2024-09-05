from marshmallow import Schema, fields, validate

class AttendanceSchema(Schema):
    """Schema for student attendance records."""
    _id = fields.Str(load_only=True)
    student_id = fields.Str(load_only=True)
    date = fields.Str()
    present = fields.Boolean()
