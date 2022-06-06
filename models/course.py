from odoo import models, fields, api


class Course(models.Model):
    _name = "rank.course"
    _description = "various courses in the institute"

    title = fields.Char('Course Title', required=True)
    code = fields.Char('Course Code', required=True)
    credit = fields.Integer('Credit Value', required=True)
    coordinator = fields.Char()
