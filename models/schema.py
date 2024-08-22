from email.policy import default
from marshmallow import Schema,fields
from enum import Enum
# from marshmallow_enum import EnumField

class PlainStudentSchema(Schema):
    id = fields.Str(dump_only= True)
    email = fields.Email(required= True)
    name= fields.Str(required=True)
    phone = fields.Int(required = True)
    dept = fields.Str(required = True)
    batch = fields.Int(required= True)
    sem = fields.Int(required = True)
    password = fields.Str(required = True,load_only = True)
    
class StudentSchema(PlainStudentSchema):
    created_at= fields.Str(required=True)
    updated_at= fields.Str()
class LoginSchema(Schema):
    email = fields.Email(required= True)
    password= fields.Str(required=True)


class PlainStaffSchema(Schema):
    id = fields.Str(dump_only= True)
    name= fields.Str(required=True)
    email = fields.Email(required= True)
    phone = fields.Int(required = True)
    dept = fields.Str(required = True)
    is_admin= fields.Bool(default= False)
    password = fields.Str(required = True,load_only = True)
    
class StaffSchema(PlainStaffSchema):
    created_at= fields.Str(required=True)
    updated_at= fields.Str()

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

