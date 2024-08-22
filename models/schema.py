from email.policy import default
from marshmallow import Schema,fields,validate
from enum import Enum
# from marshmallow_enum import EnumField

class PlainStudentSchema(Schema):
    _id = fields.Str(dump_only= True)
    email = fields.Email(required= True,validate = validate.Regexp(".*@.*student.*"))
    name= fields.Str(required=True)
    phone = fields.Int(required = True)
    dept = fields.Str(required = True)
    batch = fields.Int(required= True)
    sem = fields.Int(required = True)
    password = fields.Str(required = True,load_only = True)
    
class StudentSchema(PlainStudentSchema):
    created_at= fields.Str(required=True)
    updated_at= fields.Str()

class StudentUpdateSchema(Schema):
    email = fields.Email(validate = validate.Regexp(".*@.*student.*"))
    name= fields.Str()
    phone = fields.Int()
    dept = fields.Str()
    batch = fields.Int()
    sem = fields.Int()
    password = fields.Str()
    
class LoginSchema(Schema):
    email = fields.Email(required= True)
    password= fields.Str(required=True)


class PlainStaffSchema(Schema):
    _id = fields.Str(dump_only= True)
    name= fields.Str(required=True)
    email = fields.Email(required= True,validate = validate.Regexp(".*@.*staff.*"))
    phone = fields.Int(required = True)
    dept = fields.Str(required = True)
    is_admin= fields.Bool(default= False)
    password = fields.Str(required = True,load_only = True)
    
class StaffSchema(PlainStaffSchema):
    created_at= fields.Str(required=True)
    updated_at= fields.Str()

class StaffUpdateSchema(Schema):
    _id = fields.Str(dump_only= True)
    name= fields.Str()
    email = fields.Email(validate = validate.Regexp(".*@.*staff.*"))
    phone = fields.Int()
    dept = fields.Str()
    is_admin= fields.Bool()
    password = fields.Str(load_only=True)
    
class StaffLogin(Schema):
    staff_id = fields.Str(load_only=True)
    name = fields.Str(required = True)
    password = fields.Str(required = True)

class AttendanceSchema(Schema):
    _id= fields.Str(load_only= True)
    student_id= fields.Str(load_only= True)
    date = fields.Str()
    present = fields.Boolean()
    

class BatchSchema(Schema):
    pass

