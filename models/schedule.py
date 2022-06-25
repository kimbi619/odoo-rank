
from email.policy import default
from odoo import models, api, fields
from odoo.exceptions import Warning, RedirectWarning


class Schedule(models.Model):
    _name = "rank.schedule"
    _description = "Generate schedule for school and students"

    name = fields.Char("Title", required=True)
    when = fields.Datetime("Time")
    duration = fields.Selection([
        ('undefined', 'Undefined'),
        ('30', '30 Minutes'),
        ('an_hour', 'One Hour'),
        ('a_day', 'One Day'),
        ('a_week', 'One Week'),
    ], default="undefined", string='Duration')
    selected_departments = fields.Many2many(
        'rank.department',
        'schedule_department_rel',
        'schedule_id',
        'department_id',
        string="Selected Department",
    )
    selected_students = fields.Many2many(
        'rank.student',
        'schedule_student_rel',
        'schedule_id',
        'student_id',
        string="Selected Student",
    )

    def action_notify(self):
        print('entry cr eated ========       created')
        print(self)
        message = f'"Hi there you have a new schedule on {self.when}\
             called " {self.name} " lasting {self.duration}'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': message,
                    'type': 'success',
                    'sticky': False,
                    'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def pay_fees(self):
        print('paying fees')
        StripePortal(1000)


class StripePortal:
    def __init__(self, ammount):
        print('opened payment portal')
        print(f'you payment account is ${ammount}')
