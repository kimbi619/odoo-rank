
from odoo import fields, models, api


class StudentSchedule(models.Model):
    _name = "rank.student_schedule"
    _description = "all the assignments and schedules that a student have"

    name = fields.Char('Name')
    matricule = fields.Char('Matricule')
