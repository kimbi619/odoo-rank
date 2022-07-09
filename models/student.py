# -*- coding: utf-8 -*-

from datetime import datetime as date
from email.policy import default
import random
from urllib import request
from django.forms import ValidationError

from pkg_resources import require
from odoo import models, fields, api
from odoo.exceptions import Warning, RedirectWarning
from odoo.addons.base.models.ir_actions import IrActionsActClient
RedirectWarning


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

    library_book_ids = fields.Many2many(
        'rank.library',
        'student_library_rel',
        'student_id',
        'book_id',
        readonly=True
    )
    student_gpa = fields.Float(readonly=True)

    event = fields.Char("Event", default="Event", readonly=True)

    password = fields.Char(
        inverse='_set_password',
        invisible=True, copy=False,
        help="Generate random password for the student"
    )

    is_created = fields.Boolean('Created', default=False)

    timer = fields.Float('Time', compute="calculate_alert")

    warn = fields.Boolean(default=False)

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

    def get_user_group(self):
        student_users = self.env['res.groups'].search(
            [('id', '=', 148)]).users
        print('this is me')
        res = False
        for student_user in student_users:
            student_object = self.env['rank.student'].search(
                [('email', '=', student_user.login)])

            if student_object:
                student_object.is_created = False
        return res

    def generate_log(self):
        user_in_group = self.get_user_group()
        print(user_in_group)
        if user_in_group:
            return self
        else:
            self.is_created = True

        # self.calculate_alert()

    def calculate_alert(self):
        created_date = self.create_date
        created_time_in_sec = created_date.timestamp()
        alert_time = created_time_in_sec + 200
        actual_time = date.today()
        actual_time_in_sec = actual_time.timestamp()
        self.timer = actual_time_in_sec
        self.is_created = True

        if actual_time_in_sec >= created_time_in_sec:
            self.warn = True

    @api.model
    def create(self, vals):
        res = super(Student, self).create(vals)

        if res.matricule == 'New':
            res.matricule = self.env['ir.sequence'].next_by_code(
                'rank.student') or 'New'

        # ====CREATE NEW STUDENT IN USER ====

        new_user = self.env['res.users'].create([{
            'name': res.name,
            'email': res.email,
            'new_password': '1001',
            'password': '1001',
            'login': res.email,
        }])

        if new_user:
            res.generate_log()

        # =======================================GET ALL DEPARTMENTS AND ADD STUDENT INTO A DEPARTMENT

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

    def send_mail(self):
        template_id = self.env.ref('rank.email_template_student').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def get_student_user(self):
        return self.env['res.users'].search(
            [('login', '=', self.email)])

    def route_student(self):
        student_user = self.get_student_user()
        student_user_id = student_user.id
        return {
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': f'#id={student_user_id}&action=70&model=res.users&view_type=form&cids=1&menu_id=4'
        }
