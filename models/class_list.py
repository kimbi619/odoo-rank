
from odoo import models, api, fields


class ClassList(models.Model):
    _name = 'rank.class_list'
    _description = 'class list for this department, showing student in class'

    name = fields.Char('Name', required=True)
    matricule = fields.matricule('Matricule')
