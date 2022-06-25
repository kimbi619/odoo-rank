from odoo import models, api, fields


class DefaultStudent(models.Model):
    _name = 'rank.student_self'
    _description = 'Student dash board to access resources'
    _inherit = "rank.student"

    name = fields.Char(
        string='Name',
        default="Administrator",
    )

    matricule = fields.Char(
        string='Matricule',
        default="UBa19E0197",
    )

    profile_pic = fields.Image('Cover')

    # department_id = fields.Many2one(
    #     'rank.department', string='Department', required=True)

    is_registered = fields.Boolean(
        string='Is Registered',
    )

    def __init__(self, val1, val2):
        print('++++++++++++++++++++++')
        print('+++++++++++++++++++++')
        print(" I am inside the dashboard")

    def get_student(self):
        current_user = self.env.user

        return self.env['rank.student'].search([('email', '=', current_user.login)])

    def populate(self):
        current_student = self.get_student()

        return self

    # def get_student(self, user):

    # def create(self):
    def populated(self):
        print('---------------------')
        print('this is populated :) hahahaha ')
        print(self)
