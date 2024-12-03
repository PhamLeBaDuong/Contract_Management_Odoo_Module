from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractDocument(models.Model):
    _name = "contract.document"
    _description = "Contract Document"

    title = fields.Char()
    sideA_id = fields.Many2one('hr.employee', string="Side A")
    sideB_id = fields.Many2one('res.users', string="Side B")
    template_id = fields.Many2one('contract.template', string="Template")
    document_tag = fields.Many2many('contract.document.tag', string="Tag")
    date_of_creation = fields.Date('Date of Creation', related='template_id.date_of_creation', readonly=True)
    expiration_date = fields.Date('Expiration Date', related='template_id.expiration_date', readonly=True)
    date_of_execution = fields.Date('Date of Execution', related='template_id.date_of_execution', readonly=True)
    version = fields.Integer()
    status = fields.Selection(string="Status", selection=[('new', 'New'), ('running', 'Running'), ('expired', 'Expired'), ('canceled', 'Canceled')])
    # service_ids = fields.One2many('contract.service', 'document_id', string="Services", related='template_id.service_ids')

        # In contract.document model
    # document_term_ids = fields.One2many('contract.term', 'document_id', string="Terms")
    document_term_ids = fields.Many2many('contract.term', string="Terms")


    # @api.model
    # def create(self, vals):
    #     res = super().create(vals)
    #     if res.template_id:
    #         res.document_input_field_ids = res.template_id.input_field_ids.copy({'document_id': res.id})
    #         res.document_term_ids = res.template_id.term_ids.copy({'document_id': res.id})
    #     return res
    
    @api.depends('template_id')
    def _fetch_fields(self):
        for record in self:
            record.document_input_field_ids = record.template_id.input_field_ids
            record.document_term_ids = record.template_id.term_ids
        return True


    
