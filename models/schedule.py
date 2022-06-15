
from odoo import models, api, fields


class Schedule(models.Model):
    _name = "rank.schedule"
    _description = "Generate schedule for school and students"

    name = fields.Char("Title", required=True)
    date = fields.Date(string="Date")
    time = fields.Char("Time")
    duration = fields.Char('Duration')
    selected_departments = fields.Many2one(
        'rank.department', string="Selected Department")
    selected_students = fields.Many2one(
        'rank.student', string="Selected Student")
