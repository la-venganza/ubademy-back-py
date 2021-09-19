from flask import request, Blueprint
from flask_restful import Api, Resource

from .schemas import CourseSchema
from ..models import Course
from ...common.error_handling import ObjectNotFound

courses_v1_blue_print = Blueprint('courses_v1_blue_print', __name__)

course_schema = CourseSchema()

api = Api(courses_v1_blue_print)


class CourseListResource(Resource):
    def get(self):
        courses = Course.get_all()
        result = course_schema.dump(courses, many=True)
        return result

    def post(self):
        data = request.get_json()
        course_dict = course_schema.load(data)
        course = Course(title=course_dict['title'],
                        length=course_dict['length'],
                        year=course_dict['year'],
                        teacher=course_dict['teacher'],
                        subject=course_dict['subject']
                        )
        course.save()
        resp = course_schema.dump(course)
        return resp, 201


class CourseResource(Resource):
    def get(self, course_id):
        course = Course.get_by_id(course_id)
        if course is None:
            raise ObjectNotFound('The course doesnt not exist')
        resp = course_schema.dump(course)
        return resp


api.add_resource(CourseListResource, '/api/v1/courses/', endpoint='course_list_resource')
api.add_resource(CourseResource, '/api/v1/courses/<int:course_id>', endpoint='course_resource')
