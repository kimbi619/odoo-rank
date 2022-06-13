
from odoo import fields, models, api


class GradeStudent(models.Model):
    _name = "rank.grade"
    _description = "grade student for all his/her courses and rank the student"

    @api.depends('exam_mark', 'ca_mark')
    def get_final_mark(self):
        for x in self:
            x.final_mark = x.exam_mark + x.ca_mark

        print(self)

    @api.depends('final_mark')
    def get_grade(self):
        self.grade = ''
        for mark in self:
            if mark.final_mark >= 80:
                mark.grade = 'A'
                print(mark.grade)
            if 70 <= mark.final_mark < 80:
                mark.grade = 'B+'
            if 60 <= mark.final_mark < 70:
                mark.grade = 'B'
            if 50 <= mark.final_mark < 60:
                mark.grade = 'C'
            if 40 <= mark.final_mark < 50:
                mark.grade = 'D'
            if 35 <= mark.final_mark < 40:
                mark.grade = 'E'
            if 25 <= mark.final_mark < 35:
                mark.grade = 'F'
            if mark.final_mark < 25:
                mark.grade = 'U'
            if mark.final_mark == 0:
                mark.grade = ''

            print(mark.final_mark)

    name = fields.Char('COURSE', readonly=True)
    cv = fields.Char(string='CV', readonly=True)
    ca_mark = fields.Integer(string='CA MARK')
    exam_mark = fields.Integer(string='EXAM MARK')
    final_mark = fields.Integer(
        string='FINAL MARK', readonly=True, compute="get_final_mark")
    grade = fields.Char('GRADE', readonly=True, compute="get_grade")
    coordinator = fields.Char('COORDINATOR', readonly=True)
    matricule = fields.Char('MATRICULE')
