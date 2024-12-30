from odoo import fields, models

class ContractSignatureWizard(models.TransientModel):
    _name = 'contract.signature.wizard'
    _description = 'Contract Signature Wizard'

    input_signature = fields.Binary(string="Signature")
    document_id = fields.Many2one('contract.document', string="Contract Document", required=True)

    def action_confirm_signature(self):
        uid = self.env.uid
        if self.input_signature:
            # print(uid)
            # print(self.document_id.sideA_user_id.id)
            # print(self.document_id.sideB_user_id.id)
            if self.document_id.sideA_user_id.id == uid:
                # print(self.input_signature)
                self.document_id.write({'sideA_signature': self.input_signature})
                if self.document_id.sideB_signature:
                    self.document_id.write({'status': 'signed'})
            elif self.document_id.sideB_user_id.id == uid:
                # print(self.input_signature)
                self.document_id.write({'sideB_signature': self.input_signature})
                # print(self.document_id.sideB_signature)
                if self.document_id.sideA_signature:
                    self.document_id.write({'status': 'signed'})

