from odoo import fields, api, models


class CreateStudent(models.TransientModel):
    _name = "rank.student_wizard"
    _description = "popup to create new student"

    name = 'Add user to group'
    description = fields.Text(
        string='',
        readonly=True,
        default='Student successfully created, please verify that the student data is accurate and click validate to confirm'
    )
