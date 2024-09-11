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


from attendance import *    
from department import *
from staff import *
from student import *
from user import *
