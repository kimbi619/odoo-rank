

from odoo import models, fields, api


class StudentLine(models.Model):
    _name = 'rank.student_line'
    _description = 'Student line to appear in department view'

    student_id = fields.Many2one(
        string="student",
        comodel_name="rank.department"
    )

    student_matricule = fields.Char(
        string="matricule"
    )
