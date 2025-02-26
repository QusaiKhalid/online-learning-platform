from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from app.application.services.course_servise import CourseService
from infrastructure.repositories.course_repository import CourseRepository
from extensions import db  

# Create a new namespace for courses
course_ns = Namespace('courses', description='Course related operations')

# Define the request model for creating/updating courses
course_model = course_ns.model('Course', {
    'title': fields.String(required=True, description='Course title'),
    'description': fields.String(description='Course description'),
    'created_by': fields.Integer(required=True, description='ID of the instructor'),
    'status': fields.String(required=True, description='Course status', enum=['draft', 'published'])
})

# Register the namespace
def register_routes(api):
    api.add_namespace(course_ns)

# Initialize the repository and service
course_repository = CourseRepository(db.session)
course_service = CourseService(course_repository)

@course_ns.route('/')
class CourseResource(Resource):
    @course_ns.expect(course_model)
    def post(self):
        """Create a new course."""
        data = request.json
        course = course_service.create_course(data)
        return jsonify({'message': 'Course created successfully', 'course_id': course.id}), 201

    def get(self):
        """Get all courses."""
        courses = course_service.get_all_courses()
        return jsonify([{'id': course.id, 'title': course.title} for course in courses])

@course_ns.route('/<int:course_id>')
class CourseDetailResource(Resource):
    def get(self, course_id):
        """Get course by ID."""
        course = course_service.get_course(course_id)
        return jsonify({'title': course.title, 'description': course.description}) if course else ('Course not found', 404)

    def put(self, course_id):
        """Update a course."""
        data = request.json
        course = course_service.update_course(course_id, data)
        if not course:
            return {'message': 'Course not found'}, 404
        return {'message': 'Course updated successfully'}

    def delete(self, course_id):
        """Delete a course."""
        course_service.delete_course(course_id)
        return {'message': 'Course deleted successfully'}, 200
