
from odoo import fields, models, api
from jinja2 import Environment


class GradeStudent(models.Model):
    _name = "rank.transcript"
    _inherit = ["rank.grade", "jinja.mixin", "rank.student"]
    _description = "student result for semester"

    course_ids = fields.Char()
    library_book_ids = fields.Char()
    test = fields.Char(default="Test data", compute="compute_test")

    def get_student(self):
        current_user = self.env.user
        return self.env['rank.student'].search([('email', '=', current_user.login)])

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
            "registration_message": registration_message,
            "registration_message_type": registration_message_type,
            "email": student.email,
            "student_is_registered": student.is_registered,
            "email": student.email
        }

    def compute_test(self):
        return self.test
