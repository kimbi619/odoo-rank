# from custom.addons.rank.models.student import Student
from ast import Return
from odoo import models, fields, api


class Department(models.Model):
    _name = "rank.department"
    _description = "List of all departments available in the school"

    name = fields.Char(
        string='Department Name'
    )

    head_of_department = fields.Char(
        string='Head of Department'
    )
    number_of_student = fields.Integer(string='Number of Students')

    code = fields.Char('Department Code')

    student_list = fields.One2many(
        "rank.student_line", 'departments_id', string="Department Students")

    # ==============================SET DEPARTMENT FROM STUDENT LINE

    def write(self, vals):
        res = super(Department, self).write(vals)
        student_id = vals['student_list'][-1][2]['student_id']
        print(student_id)
        print(self)
        departments = self.env['rank.department']
        if student_id:
            for department in departments.search([]):
                print(department.name)
                for student in department.student_list:
                    print(f'{student.student_name} -- {student.matricule}')
                #     if student.student_name == self.name:
                #         student.unlink()
        #         if self.department_id == department:
        #             print('=====department found ======')
        #             self.env['rank.student_line'].create(
        #                 [{
        #                     'student_id': self.id,
        #                     'departments_id': self.department_id.id,
        #                     'student_name': self.name,
        #                     'student_matricule': self.matricule,
        #                     'student_gender': self.gender,
        #                     'student_dob': self.dob,
        #                     'student_nationality': self.nationality
        #                 }])

        return res


class StudentLine(models.Model):
    _name = 'rank.student_line'
    _description = 'Student line to appear in department view'
    _inherits = {'rank.student': 'department_id'}

    student_id = fields.Many2one(
        comodel_name="rank.student",
        string="Dataset list",
        require=True,
        ondelete="cascade"
    )

    student_name = fields.Char('Student')

    is_student_registered = fields.Boolean(
        string='Is Registered',
        index=True,
        default=True
    )

    student_matricule = fields.Char('Matricule')

    student_gender = fields.Char('Gender')

    student_dob = fields.Char('Date of Birth')

    student_nationality = fields.Char('Nationality')

    departments_id = fields.Many2one(
        comodel_name="rank.department",
        string="Department Student"
    )

    @api.onchange('student_id', 'department_id')
    def _onchange_student(self):
        self.student_matricule = self.student_id.matricule
        self.student_dob = self.student_id.dob
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
