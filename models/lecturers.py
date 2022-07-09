from odoo import models, fields, api


class Lecturers(models.Model):
    _name = "rank.lecturers"
    _description = "List of all lecturers in the university and their courses"

    name = fields.Char('Name', required=True)

    state_matricule = fields.Char('State Matricule', required=True)

    # lecturer_id = fields.Char('Matricule')

    lecturer_id = fields.Char(string='Matricule', required=True, copy=False, states={
        'draft': [('readonly', False)]}, index=True, default=lambda self: 'New')

    qualification = fields.Char('Highest qualification')

    courses = fields.Many2many(
        'rank.course',
        'lecturer_course_rel',
        'lecturer_id',
        'course_id',
        string='Lecture Courses',
    )

    salary = fields.Integer('Salary', default=200000)

    email = fields.Char('Email', required=True)

    password = fields.Char('Password')

    profile_pic = fields.Image(
        string='Profile picture',
        max_width=200,
        max_height=260,
    )

    is_created = fields.Boolean('Created', default=False)

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

    @api.model
    def create(self, vals):
        res = super(Lecturers, self).create(vals)

        if res.lecturer_id == 'New':
            res.lecturer_id = self.env['ir.sequence'].next_by_code(
                'rank.lecturers') or 'New'

        # ====CREATE NEW STUDENT IN USER ====

        new_user = self.env['res.users'].create([{
            'name': res.name,
            'email': res.email,
            'new_password': '1000',
            'password': '1000',
            'login': res.email,
        }])

        if new_user:
            res.generate_log()

        return res

    def get_lecturer_user(self):
        return self.env['res.users'].search(
            [('login', '=', self.email)])

    def route_lecturer(self):
        lecturer_user = self.get_lecturer_user()
        lecturer_user_id = lecturer_user.id
        return {
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': f'#id={lecturer_user_id}&action=70&model=res.users&view_type=form&cids=1&menu_id=4'
        }
