from odoo import models, fields, api


class Library(models.Model):
    _name = "rank.library"
    _description = "The library containing books and resources for the shool"

    name = fields.Char(string="Book Title")
    author = fields.Char('Author')
    cover = fields.Image('Cover')
    isbn = fields.Char('ISBN')
    count = fields.Integer('Quantity Available')
    description = fields.Text()
    related_department = fields.Many2many(
        'rank.department',
        'library_department_rel',
        'library_id',
        'department_id',
        string='Related Departments'
    )
    book_file = fields.Binary('The Book file')

    rating = fields.Integer('Book Ratings', default=4)

    related_course = fields.Many2many(
        'rank.course',
        'library_course_rel',
        'library_id',
        'course_id',
        string="Related Courses"
    )

    book_type = fields.Selection([
        ('e_book', 'E-Book'),
        ('physical', 'Physical Book'),
        ('audio_book', 'Audio Book'),
        ('podcast', 'Podcast'),
    ], default="e_book")

    def get_student(self):
        current_user = self.env.user

        login = current_user.login
        student = self.env['rank.student'].search(
            [('email', '=', login)])
        return student

    def loan_book(self):
        student = self.get_student()
        student.library_book_ids = self

        # user_books.__dict__(self)
