from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractDocument(models.Model):
    _name = "contract.document"
    _description = "Contract Document"

    