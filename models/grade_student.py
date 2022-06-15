
from odoo import fields, models, api
from odoo.exceptions import AccessDenied, ValidationError


class GradeStudent(models.Model):
    _name = "rank.grade"
    _description = "grade student for all his/her courses and rank the student"

    def generate_report(self):
        print('-------button active ------------------')

    @api.depends('exam_mark', 'ca_mark')
    def get_final_mark(self):
        for x in self:
            x.final_mark = x.exam_mark + x.ca_mark

    @api.depends('final_mark')
    def get_grade(self):
        self.grade = ''
        for mark in self:
            if mark.final_mark < 0:
                raise AccessDenied(
                    ("You cannot have a negative mark for " + mark.name))
            if mark.ca_mark > 30:
                raise AccessDenied(
                    ("You have an unreal CA mark for the course " + mark.name))
            if mark.exam_mark > 70:
                mark.exam_mark = 70
                raise AccessDenied(
                    ("You have an unreal Exam mark for the course " + mark.name))
            if mark.final_mark >= 80:
                mark.grade = 'A'
                mark.grade_point = 4
            if 70 <= mark.final_mark < 80:
                mark.grade = 'B+'
                mark.grade_point = 3.3
            if 60 <= mark.final_mark < 70:
                mark.grade = 'B'
                mark.grade_point = 3.0
            if 50 <= mark.final_mark < 60:
                mark.grade = 'C'
                mark.grade_point = 2.0
            if 40 <= mark.final_mark < 50:
                mark.grade = 'D'
                mark.grade_point = 1.3
            if 35 <= mark.final_mark < 40:
                mark.grade = 'E'
                mark.grade_point = 0.7
            if 25 <= mark.final_mark < 35:
                mark.grade = 'F'
                mark.grade_point = 0.3
            if mark.final_mark < 25:
                mark.grade = 'U'
                mark.grade_point = 0
            if mark.final_mark == 0:
                mark.grade = ''

    name = fields.Char('COURSE', readonly=True)
    cv = fields.Integer(string='CV', readonly=True)
    ca_mark = fields.Integer(string='CA MARK')
    exam_mark = fields.Integer(string='EXAM MARK')
    final_mark = fields.Integer(
        string='FINAL MARK', readonly=True, compute="get_final_mark")
    grade = fields.Char('GRADE', readonly=True, compute="get_grade")
    grade_point = fields.Float(readonly=True)
    coordinator = fields.Char('COORDINATOR', readonly=True)
    matricule = fields.Char('MATRICULE')

    def action_grade_me(self):
        print('------------checking student------------------')
