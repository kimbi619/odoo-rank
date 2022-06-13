# -*- coding: utf-8 -*-

from urllib import request

from pkg_resources import require
from odoo import models, fields, api


class Student(models.Model):
    _name = 'rank.student'
    _description = 'knowledge about the student in the class'

    name = fields.Char(required=True)
    matricule = fields.Char(string='Matricule', required=True, copy=False, states={
                            'draft': [('readonly', False)]}, index=True, default=lambda self: 'New')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default='male')

    is_registered = fields.Boolean('Is Registered', index=True, default=False)

    photo = fields.Image(
        string='Profile picture',
        max_width=200,
        max_height=260,
        # required=True
    )

    dob = fields.Date(string="Date of Birth")

    email = fields.Char(string="Email", required=True)

    nationality = fields.Many2one(
        'res.country', string='Nationality')

    department_id = fields.Many2one(
        'rank.department', string='Department', required=True)

    course_ids = fields.Many2many(
        'rank.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Courses'
    )

    def action_print_student(self):
        print(dir(self.env.ref('rank.computer_view_form').write))
        return self.env.ref('rank.computer_view_form').report_action(self)

    def action_check_schedule(self):
        print('------------checking student------------------')

    def action_grade_student(self):
        print('-------------grading student---------------')
        courses = self.course_ids
        matricule_present = self.env['rank.grade'].search(
            [('matricule', '=', self.matricule)])

        # course_present = self.env['rank.grade'].search([('name', '=', self.name)])

        if not matricule_present:
            for course in courses:
                self.env['rank.grade'].create([{
                    'matricule': self.matricule,
                    'name': course.name,
                    'cv': course.credit,
                    'coordinator': course.coordinator
                }])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Grade',
            'res_model': 'rank.grade',
            'view_mode': 'tree,form',
            'domain': [('matricule', '=', self.matricule)],
            'flags': {'action_buttons': False},
            'target': 'new',
        }

    @api.model
    def create(self, vals):

        if vals.get('matricule', 'New') == 'New':
            vals['matricule'] = self.env['ir.sequence'].next_by_code(
                'rank.student') or 'New'

        res = super(Student, self).create(vals)

        # =======================================GET ALL DEPARTMENTS AND ADD STUDENT INTO A DEPARTMENT

        departments = self.env['rank.department'].search([])
        for department in departments:
            if res.department_id.id == department.id:
                self.env['rank.student_line'].create(
                    [{
                        'student_id': res.id,
                        'departments_id': res.department_id.id,
                        'student_name': res.name,
                        'student_matricule': res.matricule,
                        'student_gender': res.gender,
                        'student_dob': res.dob,
                        'student_nationality': res.nationality
                    }])
                # department.number_of_student += 1
        return res

    def write(self, vals):
        res = super(Student, self).write(vals)
        # =====================================UPDATE DEPARTMENT STUDENT ON CHANGE DEPARTMENT
        departments = self.env['rank.department'].search([])
        if vals.get('department_id'):
            for department in departments:
                for student in department.student_list:
                    if student.student_matricule == self.matricule:
                        student.unlink()
                if self.department_id == department:
                    self.env['rank.student_line'].create(
                        [{
                            'student_id': self.id,
                            'departments_id': self.department_id.id,
                            'student_name': self.name,
                            'student_matricule': self.matricule,
                            'student_gender': self.gender,
                            'student_dob': self.dob,
                            'student_nationality': self.nationality
                        }])
