from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractDocument(models.Model):
    _name = "contract.document"
    _description = "Contract Document"

    title = fields.Char()
    sideA_id = fields.Many2one('hr.employee.public', string="Side A")
    # sideA_id = fields.Many2one(related='sideA_hr_id.user_id', readonly=True, string='Side A')
    sideA_name = fields.Char(related='sideA_id.name')
    sideA_birthday = fields.Date(related='sideA_id.employee_id.birthday')
    sideA_work_email = fields.Char(related='sideA_id.work_email')
    sideA_work_phone = fields.Char(related='sideA_id.work_phone')
    sideA_address_id = fields.Many2one(related='sideA_id.address_id')
    sideA_gender = fields.Selection(related='sideA_id.employee_id.gender', groups="hr.group_hr_user")
    
    # sideA_private_street = fields.Char(related='sideA_id.private_street', readonly=True)
    # sideA_private_street2 = fields.Char(related='sideA_id.private_street2', readonly=True)
    # sideA_private_city = fields.Char(related='sideA_id.private_city', readonly=True)
    # sideA_private_country_id = fields.Many2one(related='sideA_id.private_country_id', readonly=True)

    sideB_user_id = fields.Many2one('res.users', string="Side B", default = lambda self: self.env.user, index=True, tracking=True)
    sideB_id = fields.Many2one(related='sideB_user_id.employee_id', string='Side B')
    sideB_name = fields.Char(related='sideB_id.name')
    sideB_birthday = fields.Date(related='sideB_id.birthday')
    sideB_work_phone = fields.Char(related='sideB_user_id.work_email')
    sideB_work_email = fields.Char(related='sideB_user_id.work_phone')
    sideB_address_id = fields.Many2one(related='sideB_id.address_id')
    sideB_gender = fields.Selection(related='sideB_user_id.gender', groups="hr.group_hr_user")

    template_id = fields.Many2one('contract.template', string="Template")
    # dynamic_input_values = fields.Json(string="Dynamic Input Values")
    document_tag = fields.Many2many('contract.document.tag', string="Tag")
    date_of_creation = fields.Date('Date of Creation', default = fields.Date.today())
    expiration_date = fields.Date('Expiration Date', default = fields.Date.today() + timedelta(days=365))
    date_of_execution = fields.Date('Date of Execution')
    version = fields.Integer()
    
    status = fields.Selection(string="Status", selection=[('new', 'New'), ('waiting', 'Waiting'), ('signed', 'Signed'), ('canceled', 'Canceled')], default='new')
    # service_ids = fields.One2many('contract.service', 'document_id', string="Services", related='template_id.service_ids')

        # In contract.document model
    # document_term_ids = fields.One2many('contract.term', 'document_id', string="Terms")
    document_term_ids = fields.Many2many('contract.term', string="Terms")
    input_fields_ids = fields.Many2many('contract.input.field', string="Input Fields")
    term_content_ids = fields.Many2many('contract.term.content', string="Contents")

    # @api.model
    # def create(self, vals):
    #     res = super().create(vals)
    #     if res.template_id:
    #         res.document_input_field_ids = res.template_id.input_field_ids.copy({'document_id': res.id})
    #         res.document_term_ids = res.template_id.term_ids.copy({'document_id': res.id})
    #     return res
    
    # @api.model
    # def create(self, vals):
    #     res = super(ContractDocument, self).create(vals)
    #     if res.template_id:
    #         for term in res.template_id.term_ids:
    #             # term.copy({'document_id': res.id, 'template_id': False}) # Remove link to template
    #     return res
    
    @api.onchange('template_id')
    def _fetch_fields(self):
            
        if self.template_id:
            self.document_term_ids = [(5,0,0)]

            for term in self.template_id.term_ids:
                self.document_term_ids = [(0, 0, {
                    'name': term.name,
                    # 'input_field_ids': [(4, x) for x in term.input_field_ids.ids],
                    # 'content_ids': [(4,x) for x in term.content_ids.ids],
                    'input_field_ids': [(6, 0, term.input_field_ids.ids)],
                    'content_ids': [(6, 0, term.content_ids.ids)],
                    'description': term.description,
                })]
        else:
            self.document_term_ids = [(5,0,0)]
            self.input_fields_ids = [(5,0,0)]
            self.term_content_ids = [(5,0,0)]


    def print_contract(self):
        return self.env.ref('contract_management.contract_document_report').report_action(self)


# class IrUiView(models.Model):
#     _inherit = 'ir.ui.view'
#     type = fields.Selection(selection_add=[('custom_view', "Custom View")])

# class IrActionsActWindowView(models.Model):
#     """
#        Extends the base 'ir.actions.act_window.view' model to include
#        a new view mode called 'grid'.
#    """
#     _inherit = 'ir.actions.act_window.view'
#     view_mode = fields.Selection(selection_add=[('custom_view', "Custom View")],
#                                  ondelete={'custon_view': 'cascade'})


    # @api.onchange('sideA_hr_id')
    # def _fetch_sideA(self):
    #     if self.sideA_hr_id:
    #         self.sideA_id = self.sideA_hr_id.user_id
    #         self.sideA_birthday = self.sideA_id.birthday
    #         self.sideA_work_email = self.sideA_id.work_email
    #         self.sideA_work_phone = self.sideA_id.work_phone
    #         self.sideA_address_id = self.sideA_id.address_id
    #         self.sideA_gender = self.sideA_id.gender