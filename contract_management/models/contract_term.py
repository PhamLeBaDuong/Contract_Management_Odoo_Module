from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractTerm(models.Model):
    _name = "contract.term"
    _description = "Contract Term"

    name = fields.Char()
    # input_field_ids = fields.One2many('contract.input.field', 'term_id', string="Input Fields")
    # content_ids = fields.One2many('contract.term.content', 'term_id', string="Contents")
    input_field_ids = fields.Many2many('contract.input.field', string="Input Fields")
    content_ids = fields.Many2many('contract.term.content', string="Contents")
    # template_id = fields.Many2one('contract.template', string="Template")
    # document_id = fields.Many2one('contract.document', string="Document")
    sequence = fields.Integer()
    description = fields.Text()