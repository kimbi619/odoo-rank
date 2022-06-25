# -*- coding: utf-8 -*-
{
    'name': "classrank",

    'summary': """A school ranking system""",

    'description': """
        generates student report card and rank them in a class based on marks, giving them their gpa/average for the semester/term
    """,

    'author': "TIDE",
    'website': "http://www.nkda.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        # 'views/student_dashboard.xml',
        # 'data/mail_template.xml',
        'views/lecturers.xml',
        'views/library.xml',
        'views/student.xml',
        'views/student_self.xml',
        'views/schedule.xml',
        'views/grade_student.xml',
        'views/department.xml',
        'views/course.xml',
        'report/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
