from odoo import models, api, fields


class DefaultStudent(models.Model):
    _name = 'rank.student_self'
    _description = 'Student dash board to access resources'

    name = fields.Char('Name', readonly=True,
                       default="Administrator", compute='get_property')
    matricule = fields.Char('Matricule', readonly=True, default="UBa19E0197")
    profile_pic = fields.Image('Profile_pic', readonly=True)
    is_registered = fields.Boolean('Is Registered', readonly=True)

    def get_property(self):
        current_user = self.env.user
        current_student = self.env['rank.student'].search(
            [('email', '=', current_user.login)])

        self.name = current_student.name
        self.matricule = current_student.matricule
        print('logged in user')
        print(self.env.user.name)
        print(self.env.user.login)
        print(current_student)
