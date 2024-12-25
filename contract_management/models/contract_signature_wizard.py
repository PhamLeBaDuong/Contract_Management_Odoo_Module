from odoo import fields, models

class ContractSignatureWizard(models.TransientModel):
    _name = 'contract.signature.wizard'
    _description = 'Contract Signature Wizard'

    input_signature = fields.Text(string="Signature", required=True)
    document_id = fields.Many2one('contract.document', string="Contract Document", required=True)

    def action_confirm_signature(self):
        uid = self.env.uid
        if self.document_id.sideA_user_id == uid:
            self.document_id.write({'sideA_signature': self.input_signature})  # Store and sign
        else:
            self.document_id.write({'sideB_signature': self.input_signature})  # Store and sign

