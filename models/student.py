# -*- coding: utf-8 -*-

from urllib import request
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

    photo = fields.Binary('Photo')

    dob = fields.Date(string="Date of Birth")

    email = fields.Char(string="Email", required=True)

    nationality = fields.Many2one(
        'res.country', string='Nationality')

    department_id = fields.Many2one(
        'rank.department', string='Department', required=True)

    @api.model
    def create(self, vals):
        # if not vals.get('name'):
        # =======================================CASCADE DATA

        if vals.get('matricule', 'New') == 'New':
            vals['matricule'] = self.env['ir.sequence'].next_by_code(
                'rank.student') or 'New'

        res = super(Student, self).create(vals)

        # =======================================GET ALL DEPARTMENTS AND ADD STUDENT INTO A DEPARTMENT

        departments = self.env['rank.department']
        for department in departments.search([]):
            if res.department_id.name == department.name:
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
        departments = self.env['rank.department']
        if vals.get('department_id'):
            for department in departments.search([]):
                for student in department.student_list:
                    if student.student_name == self.name:
                        student.unlink()
                if self.department_id == department:
                    print('=====department found ======')
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
