from marshmallow import fields

from app.ext import ma


class CourseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    length = fields.Integer()
    year = fields.Integer()
    teacher = fields.String()
    subject = fields.String()
