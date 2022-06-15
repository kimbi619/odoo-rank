from odoo import models, fields, api


class Course(models.Model):
    _name = "rank.course"
    _description = "various courses in the institute"

    name = fields.Char('Course Title', required=True)
    code = fields.Char('Course Code', required=True)
    credit = fields.Integer('Credit Value', required=True)
    coordinator = fields.Char()
    department_ids = fields.Many2many(
        'rank.department',
        'department_course_rel',
        'course_id',
        'department_id',
        string='Departments'
    )
    student_ids = fields.Many2many(
        'rank.student',
        'student_course_rel',
        'course_id',
        'student_id',
        string='Students',
        readonly=True
    )
