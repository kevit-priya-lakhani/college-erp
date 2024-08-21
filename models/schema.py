from marshmallow import Schema,fields
from enum import Enum
from marshmallow_enum import EnumField

class StudentSchema(Schema):
    id = fields.Str(dump_only= True)
    name= fields.Str(required=True)
    phone = fields.Int(required = True)
    dept = fields.Str(required = True)
    batch = fields.Int(required= True)
    sem = fields.Str(required = True)
    created_at= fields.Str(required=True)
    updated_at= fields.Str()

class StaffSchema(Schema):
    id = fields.Str(dump_only= True)
    name= fields.Str(required=True)
    phone = fields.Int(required = True)
    dept = fields.Str(required = True)
    created_at= fields.Str(required=True)
    updated_at= fields.Str()
    is_admin= fields.Bool(required= True)

class StaffLogin(Schema):
    staff_id = fields.Str(load_only=True)
    name = fields.Str(required = True)
    password = fields.Str(required = True)

class AttendanceSchema(Schema):
    student_id= fields.Str(load_only= True)
    date = fields.DateTime()
    present = fields.Boolean()
    

class BatchSchema(Schema):
    pass

