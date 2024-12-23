from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractTermDisplay(models.Model):
    _name = "contract.term.display"
    _description = "Contract Term Display"

    name = fields.Char(string="Title")
    content_ids = fields.Many2many('contract.term.content', string="Contents")