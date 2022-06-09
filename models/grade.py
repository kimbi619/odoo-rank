
from odoo import fields, models, api


class StudentSchedule(models.Model):
    _name = "rank.grade"
    _description = "grade student for all his/her courses and rank the student"

    name = fields.Char('Course')
    grade = fields.Char('Mark')
    coordinator = fields.Char('Coordinator')
