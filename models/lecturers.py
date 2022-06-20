from odoo import models, fields, api


class Lecturers(models.Model):
    _name = "rank.lecturers"
    _description = "List of all lecturers in the university and their courses"

    name = fields.Char('Name')

    state_matricule = fields.Char('Matricule')

    lecturer_id = fields.Char('Matricule')

    qualification = fields.Char('Highest qualification')

    courses = fields.Many2many(
        'rank.course',
        'lecturer_course_rel',
        'lecturer_id',
        'course_id',
        string='Lecture Courses'
    )

    salary = fields.Integer('Salary')

    password = fields.Char('Password')

    profile_pic = fields.Image(
        string='Profile picture',
        max_width=200,
        max_height=260,
    )
