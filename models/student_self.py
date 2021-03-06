from odoo import models, api, fields
from jinja2 import Environment


class DefaultStudent(models.Model):
    _name = 'rank.student_self'
    _inherit = ['rank.student', 'jinja.mixin']
    _description = 'Student dash board to access resources'

    course_ids = fields.Char()
    library_book_ids = fields.Char()

    def view_data(self):
        student = self.get_student()
        registration_message = ''
        registration_message_type = 'danger'
        if student.is_registered:
            registration_message = "Congratulation!!! <br /> <strong>you have competed your tuition </strong> "
            registration_message_type = 'success'
        else:
            registration_message = "You haven't completed your registration. <br /><strong> Select method to pay tuition below </strong><br />"

        return {
            "env": self.env,
            "name": student.name,
            "matricule": student.matricule,
            "nationality": student.nationality,
            "courses": student.course_ids,
            "registration_message": registration_message,
            "registration_message_type": registration_message_type,
            "email": student.email,
            "first_name": student.name,
            "gender": student.gender,
            "dob": student.dob,
            "student_is_registered": student.is_registered

        }

    def get_student(self):
        current_user = self.env.user
        return self.env['rank.student'].search([('email', '=', current_user.login)])

    def pay_with_mtn_momo(self):
        print('payent api')
