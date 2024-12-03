from datetime import timedelta
from odoo import fields, models

class ContractTag(models.Model):
    _name = "contract.document.tag"

    color = fields.Integer()
    name = fields.Char(required=True)

    