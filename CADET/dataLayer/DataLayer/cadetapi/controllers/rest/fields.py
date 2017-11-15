""" These dictionaries define the return values from the appropriate API
    calls. These are broken up into a separate file in order for the other
    APIs to make use of all the fields, in case an API needs to return a
    nested structure. More information ca be found at:
    https://flask-restful.readthedocs.io/en/0.3.6/fields.html
"""

from flask_restful import fields

comment_fields = {
    'id' : fields.Integer(),
    'anon_id' : fields.Integer(),
    'comment' : fields.String(),
    'course_id' : fields.Integer(),
    'instr_id' : fields.Integer(),
    'instr_com' : fields.String(),
    'timestamp' : fields.DateTime(dt_format='iso8601')
}

#if foreign keys
#course_fields = {
#    'id' : fields.Integer(),
#    'department' : fields.String(),
#    'program' : fields.String(),
#    'course' : fields.String(),
#    'section' : fields.Integer(),
#    'year' : fields.Integer(),
#    'semester' : fields.Integer()
#}
#instructor_fields = {
#    'id' : fields.Integer(),
#    'first_name' : fields.String(),
#    'last_name' : fields.String()
#}
#comment_fields = {
#    'id' : fields.Integer(),
#    'anon_id' : fields.Integer(),
#    'comment' : fields.String(),
#    'course_id' : fields.List(fields.Nested(nested_course_id)),
#    'instr_id' : fields.List(fields.Nested(nested_instr_id)),
#    'instr_com' : fields.String(),
#    'timestamp' : fields.DateTime(dt_format='iso8601')
#}
#endif
#or 'instr_id' : fields.String(attribute=lambda x: x.Instructor.last_name)

# Use Nested() for a many-to-many relationship
# Use lambda construct for one-to-many relationship
