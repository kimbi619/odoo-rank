from odoo import models, fields, api


class Library(models.Model):
    _name = "rank.library"
    _description = "The library containing books and resources for the shool"

    name = fields.Char(string="Book Title", required=True)

    author = fields.Char(string="Author")

    cover = fields.Image(string="Cover")

    isbn = fields.Char(string='ISBN')

    count = fields.Integer('Ammount in stock')

    description = fields.Char('description of book')

    related_department = fields.Many2many(
        'rank.department',
        'library_department_rel',
        'library_id',
        'department_id',
        string='Related Departments'
    )

    related_course = fields.Many2many(
        'rank.course',
        'library_course_rel',
        'library_id',
        'course_id',
        string="Related Courses"
    )
