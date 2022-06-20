from odoo import models, api, fields


class DefaultStudent(models.Model):
    _name = 'rank.student_self'
    _description = 'Student dash board to access resources'

    name = fields.Char(
        string='Name',
        readonly=True,
        default="Administrator",
        compute='get_property'
    )

    matricule = fields.Char(
        string='Matricule',
        readonly=True,
        default="UBa19E0197"
    )

    profile_pic = fields.Image(
        string='Profile_pic',
        readonly=True
    )

    is_registered = fields.Boolean(
        string='Is Registered',
        readonly=True,
        compute="check_registered"
    )

    def get_property(self):
        current_user = self.env.user
        current_student = self.env['rank.student'].search(
            [('email', '=', current_user.login)])

        self.name = current_student.name
        self.matricule = current_student.matricule
        print('logged in user')
        print(self.env.user.name)
        print(self.env.user.login)

    def check_registered(self):
        self.is_registered = False
        if self.is_registered:
            print('student is registered')
        else:
            print('studnet NOT REGISTERED')
