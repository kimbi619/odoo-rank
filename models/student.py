# -*- coding: utf-8 -*-

from email.policy import default
import random
from urllib import request
from django.forms import ValidationError

from pkg_resources import require
from odoo import models, fields, api
from odoo.exceptions import Warning


class Student(models.Model):
    _name = 'rank.student'
    _description = 'knowledge about the student in the class'
    _order = "student_gpa desc"

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

    position = fields.Char('Position', default='Ungraded', readonly=True,
                           compute="generate_position")

    department_id = fields.Many2one(
        'rank.department', string='Department', required=True)

    course_ids = fields.Many2many(
        'rank.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Courses'
    )
    student_gpa = fields.Float(readonly=True)

    event = fields.Char("Event", default="Event", readonly=True)

    password = fields.Char(
        compute='generate_password', inverse='_set_password',
        invisible=True, copy=False,
        required=True,
        help="Generate random password for the student")

    grade_status = fields.Selection(
        [('none', 'None'),
         ('generated', 'Generated'),
         ('partial', 'Partial'),
         ('complete', 'Complete')
         ], default="none", string="Grade Status")

    # ==============================CALCULATE STUDENT GPA==================

    def action_student_average(self):
        self.student_gpa = -1
        current_student_courses = self.env['rank.grade'].search(
            [('matricule', '=', self.matricule)])
        totalMark = 0
        totalCV = 0
        totalCourse = len(current_student_courses)
        if totalCourse == 0:
            raise Warning("Student has not registered any courses")
            return
        for grade in current_student_courses:
            credit = grade.grade_point * grade.cv
            totalMark += credit
            totalCV += grade.cv
        self.student_gpa = totalMark/totalCV
        self.grade_status = "complete"

    # =======================CALCULATE STUDENT POSITION==================
    def generate_position(self):
        graded_students = self.env['rank.student'].search(
            [('student_gpa', '!=', 0.00)])
        class_count = len(graded_students)
        self.position = ''
        position = 0
        for current_student in graded_students:
            position += 1
            current_student.position = str(position)

    # ===================== CALCULATE STUDENT SCHEDULE==================
    def action_check_schedule(self):
        print(self)
        print('------------checking student------------------')

    # ========== GENERATE RANDOM PASSWORD FOR STUDENT ==================
    def generate_password(self):
        password = ''
        for i in range(0, 6):
            char = random.randint(0, 9)
            password += str(char)
        self.password = password

    def action_grade_student(self):
        courses = self.course_ids
        matricule_present = self.env['rank.grade'].search(
            [('matricule', '=', self.matricule)])

        self.grade_status = "generated"
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
            'flags': {'action_buttons': False, 'create': False},
            'target': 'new',
        }

    @api.model
    def create(self, vals):

        if vals.get('matricule', 'New') == 'New':
            vals['matricule'] = self.env['ir.sequence'].next_by_code(
                'rank.student') or 'New'

        res = super(Student, self).create(vals)
        right = self.env['res.groups'].search([('id', '=', 44)])

        new_user = self.env['res.users'].create([{
            'name': res.name,
            'email': res.email,
            'new_password': '1001',
            'password': '1001',
            'login': res.email,
        }])
        group_ids = new_user.groups_id.search([('id', '=', 21)])
        group_ids.unlink()
        new_user.create(right[0])
        # group_ids.create([
        #     {
        #         'name': 'Student',
        #         'model_access': right.model_access,
        #         'rule_groups': right.rule_groups,
        #         'menu_access': right.menu_access,
        #         'view_access': right.view_access,
        #         'category_id': right.category_id.id,
        #         'color': right.color,
        #         'full_name': right.full_name,
        #         'share': right.share
        #     }
        # ])

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
