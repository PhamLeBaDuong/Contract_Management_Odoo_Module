from odoo import fields, models


class ContractTemplate(models.Model):
    _name = 'contract.template'
    _description = 'Contract Template'

    name = fields.Char()
    template_tag_ids = fields.Many2many('contract.document.tag', string="Tags")
    # date_of_execution = fields.Date()  
    # date_of_creation = fields.Date()
    # expiration_date = fields.Date()
    term_ids = fields.Many2many('contract.term', string="Terms")
    document_ids = fields.One2many('contract.document', 'template_id', string="Documents")


    
    