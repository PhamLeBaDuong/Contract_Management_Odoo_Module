from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractInputField(models.Model):
    _name = "contract.input.field"
    _description = "Contract input field"

    name = fields.Char()
    field_type = fields.Selection([('char','Char'), ('date','Date'),('integer', 'Integer'),('selection','Selection')], required = True)
    required=fields.Boolean()
    selecction_options = fields.Char()
    # term_id = fields.Many2one('contact.term', string = 'Term')
    

    