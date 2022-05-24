from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from flask import request
from .schema import AssignmentGradeSchema, AssignmentSchema
teacher_assignment_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignment_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def assignment_teacher(p):
    print('hello')
    print(p)
    print(p.teacher_id, p.user_id)
    teacher_assignments = Assignment.get_assignment_by_teacher(p.teacher_id) #method made in models.py in assignment.
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True) 

    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def teacher_grade_assignment(p, incoming_payload):
    print(p)
    data = request.json
    print(data)
    grade_ = data['grade']
    
    submit_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.assign_grade(
        teacher_id = p.teacher_id,
        grade = grade_,
        principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

    return APIResponse.respond(data=graded_assignment_dump)