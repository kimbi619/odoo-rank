from odoo import models, fields, api


class Blog(models.Model):
    _name = 'rank.blog'
    _description = 'school blog to post news about the school by anyone in the school'

    title = fields.Char(string='Title')
    cover_image = fields.Image(string='Cover Image')
    content = fields.Text(string='Content')
