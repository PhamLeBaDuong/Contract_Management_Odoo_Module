from odoo import fields, models


class ContactTermContent(models.Model):
    _name = 'contract.term.content'
    _description = 'Contract Term Content'

    content = fields.Text()


    