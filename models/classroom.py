
from odoo import fields, models, api


class GradeStudent(models.Model):
    _name = "rank.classroom"
    # _inherit = "rank.course"
    _description = "elearning classroom"

    name = fields.Char('Course Title')
