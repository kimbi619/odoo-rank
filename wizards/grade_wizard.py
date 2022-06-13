from odoo import fields, api, models


class GradeAStuent(models.TransientModel):
    _name = "Grade.student"
    _description = "popup to grade a student"
