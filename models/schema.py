"""
This module defines Marshmallow schemas for serialization and deserialization of 
student and staff data, as well as for handling login, attendance, and department records.

Schemas:
- `PlainStudentSchema`: Defines the schema for student data without timestamps.
- `StudentSchema`: Extends `PlainStudentSchema` with creation and update timestamps.
- `StudentUpdateSchema`: Defines the schema for updating student data.
- `LoginSchema`: Defines the schema for user login credentials.
- `PlainStaffSchema`: Defines the schema for staff data without timestamps.
- `StaffSchema`: Extends `PlainStaffSchema` with creation and update timestamps.
- `StaffUpdateSchema`: Defines the schema for updating staff data.
- `StaffLogin`: Defines the schema for staff login, primarily used for authentication.
- `AttendanceSchema`: Defines the schema for attendance records.
- `DepartmentSchema`: Defines the schema for department records.
- `BatchSchema`: Placeholder schema for batch data (currently not implemented).

Dependencies:
- Marshmallow for schema definition and validation.
- Enum for handling enumerations (imported but not used).

Classes:
- `PlainStudentSchema`: Base schema for student records.
- `StudentSchema`: Schema for student records with timestamps.
- `StudentUpdateSchema`: Schema for updating student information.
- `LoginSchema`: Schema for user login data.
- `PlainStaffSchema`: Base schema for staff records.
- `StaffSchema`: Schema for staff records with timestamps.
- `StaffUpdateSchema`: Schema for updating staff information.
- `StaffLogin`: Schema for staff login credentials.
- `AttendanceSchema`: Schema for recording student attendance.
- `DepartmentSchema`: Schema for department information.
- `BatchSchema`: Placeholder schema (currently not in use).
"""

from email.policy import default
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

class LoginSchema(Schema):
    """Schema for user login credentials."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

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

class AttendanceSchema(Schema):
    """Schema for student attendance records."""
    _id = fields.Str(load_only=True)
    student_id = fields.Str(load_only=True)
    date = fields.Str()
    present = fields.Boolean()

class DepartmentSchema(Schema):
    """Schema for department records."""
    _id = fields.Str(load_only=True)
    name = fields.Str(required=True, unique=True)
    created_at = fields.Str()
    updated_at = fields.Str()

class BatchSchema(Schema):
    """Placeholder schema for batch data (currently not implemented)."""
    pass
