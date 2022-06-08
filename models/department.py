# from custom.addons.rank.models.student import Student
from ast import Return

from pkg_resources import require
from odoo import models, fields, api


class Department(models.Model):
    _name = "rank.department"
    _description = "List of all departments available in the school"

    @api.depends('student_list')
    def students_in_list(self):
        self.number_of_student = len(self.student_list)

    name = fields.Char(
        string='Department Name',
        required=True
    )

    head_of_department = fields.Char(
        string='Head of Department',
        required=True
    )
    number_of_student = fields.Integer(
        compute="students_in_list",
        string='Number of Students'
    )

    code = fields.Char('Department Code', require=True)

    student_list = fields.One2many(
        "rank.student_line", 'departments_id',
        string="Department Students", copy=False
    )

    # ==============================SET DEPARTMENT FROM STUDENT LINE

    def write(self, vals):
        res = super(Department, self).write(vals)
        student = vals['student_list'][-1][-1]
        departments = self.env['rank.department']
        if student['student_matricule'] or student['student_id']:
            for department in departments.search([]):
                if department.id != self.id:
                    for studentLine in department.student_list:
                        if studentLine.student_matricule == student['student_matricule']:
                            studentLine.unlink()

            # self.env['rank.student_line'].create(newStudent)
            # self.env['rank.student_line'].create(
            #     [{
            #         'student_id': newStudent.id,
            #         'departments_id': newStudent.department_id.id,
            #         'student_name': newStudent.name,
            #         'student_matricule': newStudent.matricule,
            #         'student_gender': newStudent.gender,
            #         'student_dob': newStudent.dob,
            #         'student_nationality': newStudent.nationality
            #     }])

        return res


class StudentLine(models.Model):
    _name = 'rank.student_line'
    _description = 'Student line to appear in department view'
    # _inherits = {'rank.student': 'department_id'}

    student_id = fields.Many2one(
        comodel_name="rank.student",
        string="Dataset list",
        required=True,
        readonly=True,
        ondelete="cascade"
    )

    student_name = fields.Char('Student')

    is_student_registered = fields.Boolean(
        string='Is Registered',
        index=True,
        readonly=True,
        default=True
    )

    student_matricule = fields.Char('Matricule', readonly=True)

    student_gender = fields.Char('Gender', readonly=True)

    student_email = fields.Char('Email', readonly=True)

    student_dob = fields.Char('Date of Birth', readonly=True)

    student_nationality = fields.Char('Nationality', readonly=True)

    departments_id = fields.Many2one(
        comodel_name="rank.department",
        readonly=True,
        string="Department Student"
    )

    @api.onchange('student_id', 'department_id')
    def _onchange_student(self):
        self.student_matricule = self.student_id.matricule
        self.student_dob = self.student_id.dob
        self.student_email = self.student_id.email
        self.student_gender = self.student_id.gender
        self.student_nationality = self.student_id.nationality
        self.is_student_registered = self.student_id.is_registered

    # @api.model
    # def default_get(self, students):
    #     res = super(Student, self).default_get(students)
    #     student_line = []
    #     student_rec = self.env['rank.student'].search([])
    #     for rec in student_rec:
    #         print('==================Model================')
    #         print('=======================================')
    #         print(rec)

    # |
    # |
    # |
    # |
    # |
    # |
    # |
    # |
    # |
    # |

    # |
    # |
    # |

    #
    #
    #
    # @api.multi
    # def open_second_class(self):
    #     ac = self.env['ir.model.data'].xmlid_to_res_id(
    #         'rank.student.view_mymodule_department_id_form', raise_if_not_found=True)
    #     for rec in self:
    #         tbl1 = rec.department_id
    #         return rec
    # @api.onchange('department_id')
    # def onchange_student(self):
    #     for student in self:
    #         return student
