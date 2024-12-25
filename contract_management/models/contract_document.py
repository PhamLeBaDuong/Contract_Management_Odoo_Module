from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractDocument(models.Model):
    _name = "contract.document"
    _inherit =["portal.mixin"]
    _description = "Contract Document"

    title = fields.Char()
    sideA_user_id = fields.Many2one('res.users', string="Side A", index=True, tracking=True)
    # sideA_id = fields.Many2one(related='sideA_user_id.employee_id', string='Side A')
    sideA_id = fields.Many2one(related='sideA_user_id.employee_id', string='Side A')
    
    # sideA_id = fields.Many2one(related='sideA_hr_id.user_id', readonly=True, string='Side A')
    sideA_name = fields.Char(related='sideA_id.name', readonly=False)
    # sideA_name = fields.Char()
    sideA_birthday = fields.Date(related='sideA_id.birthday', readonly=False)
    # sideA_birthday = fields.Date()
    sideA_work_email = fields.Char(related='sideA_id.work_email', readonly=False)
    # sideA_work_email = fields.Char()
    sideA_work_phone = fields.Char(related='sideA_id.work_phone', readonly=False)
    # sideA_work_phone = fields.Char()
    sideA_address_id = fields.Many2one(related='sideA_id.address_id', readonly=False)
    # sideA_address_id = fields.Many2one('res.partner')
    # sideA_gender = fields.Selection(related='sideA_id.employee_id.gender', groups="hr.group_hr_user")
    # sideA_gender = fields.Selection()
    sideA_signature = fields.Char()
    
    # sideA_private_street = fields.Char(related='sideA_id.private_street', readonly=True)
    # sideA_private_street2 = fields.Char(related='sideA_id.private_street2', readonly=True)
    # sideA_private_city = fields.Char(related='sideA_id.private_city', readonly=True)
    # sideA_private_country_id = fields.Many2one(related='sideA_id.private_country_id', readonly=True)

    sideB_user_id = fields.Many2one('res.users', string="Side B", default = lambda self: self.env.user, index=True, tracking=True, readonly=True)
    sideB_id = fields.Many2one(related='sideB_user_id.employee_id', string='Side B')
    sideB_name = fields.Char(related='sideB_id.name')
    sideB_birthday = fields.Date(related='sideB_id.birthday')
    sideB_work_phone = fields.Char(related='sideB_user_id.work_email')
    sideB_work_email = fields.Char(related='sideB_user_id.work_phone')
    sideB_address_id = fields.Many2one(related='sideB_id.address_id')
    # sideB_gender = fields.Selection(related='sideB_user_id.gender', groups="hr.group_hr_user")
    sideB_signature = fields.Char()


    template_id = fields.Many2one('contract.template', string="Template")
    # dynamic_input_values = fields.Json(string="Dynamic Input Values")
    document_tag = fields.Many2many('contract.document.tag', string="Tag")
    date_of_creation = fields.Date('Date of Creation', default = fields.Date.today(), readonly=True)
    expiration_date = fields.Date('Expiration Date', default = fields.Date.today() + timedelta(days=365))
    date_of_execution = fields.Date('Date of Execution')
    version = fields.Integer()
    
    has_product = fields.Boolean()
    product_name = fields.Char(string="Product Name")
    product_price = fields.Integer(string="Product Value")
    product_description = fields.Text(string="Product Description")
    payment_term = fields.Selection(string="Payment Term", selection=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually'), ('one_time', 'One Time')], default='one_time')
    
    status = fields.Selection(string="Status", selection=[('new', 'New'), ('sent', 'Sent'), ('signed', 'Signed'), ('canceled', 'Canceled')], default='new')
    state = fields.Selection(string="State", selection=[('draft','Draft'), ('posted','Posted')], default='draft')

    
    
    # service_ids = fields.One2many('contract.service', 'document_id', string="Services", related='template_id.service_ids')

        # In contract.document model
    # document_term_ids = fields.One2many('contract.term', 'document_id', string="Terms")
    document_term_ids = fields.Many2many('contract.term', string="Terms")
    input_fields_ids = fields.Many2many('contract.input.field', string="Input Fields")
    term_content_ids = fields.Many2many('contract.term.content', string="Contents")
    document_term_display_ids = fields.Many2many('contract.term.display', 'document_id', string="Terms", readonly=True)
    

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
    
    # @api.onchange('sideA_user_id')
    # def _fetch_sideA(self):
    #     if self.sideA_user_id:
    #         # print(self.sideA_user_id)
    #         self.sideA_id = self.sideA_user_id.employee_id
    #         self.sideA_birthday = self.sideA_id.birthday
    #         self.sideA_work_email = self.sideA_id.work_email
    #         self.sideA_work_phone = self.sideA_id.work_phone
    #         self.sideA_address_id = self.sideA_id.address_id
    #         # self.sideA_gender = self.sideA_id.gender
    
    @api.onchange('template_id')
    def _fetch_fields(self):            
        if self.template_id:
            self.document_term_ids = [(5,0,0)]

            for term in self.template_id.term_ids:
                self.document_term_ids = [(0, 0, {
                    'name': term.name,
                    'input_field_ids': [(4, x) for x in term.input_field_ids.ids],
                    'content_ids': [(4, x) for x in term.content_ids.ids],
                    # 'input_field_ids': [(6, 0, term.input_field_ids.ids)],
                    # 'content_ids': [(6, 0, term.content_ids.ids)],
                    'description': term.description,
                })]
        else:
            self.document_term_ids = [(5,0,0)]
            
    def print_contract(self):
        self.ensure_one()
        # return {
        #     'type': 'ir.actions.act_url',
        #     'target': 'self',
        #     'url': self.get_portal_url(),
        # }
        # return {
        #     'type': 'ir.actions.report',
        #     'report_type': 'qweb-pdf',
        #     'report_name': 'contract_management.contract_document_report',
        #     'report_file': 'contract_management.contract_document_report',
        #     'data': {'ids': self.ids, 'model': 'contract.document'},
        #     'context': self.env.context,
        # }
        return self.env.ref('contract_management.action_contract_document_report').report_action(self)
    
    def send_contract(self):
        self.ensure_one()
        return self.write({'status': 'sent'})
    
    def sign_contract(self):
        self.ensure_one()
        # Launch the wizard instead of directly writing status
        return {
            'name': 'Confirm Signature',
            'type': 'ir.actions.act_window',
            'res_model': 'contract.signature.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('contract_management.contract_signature_wizard_view_form').id, 
            'target': 'new',
            'context': {'default_document_id': self.id},
        }
        
    @api.onchange('sideA_signature','sideB_signature')
    def check_sign_status(self):
        if(not self.sideA_signature and not self.sideB_signature):
            return self.write({'status': 'signed'})
    

    # @api.model
    # def create(self, vals_list):
    #     records = super().create(vals_list)
    #     for record in records:
    #         record.state='drafted'
    #     return records
    
    def action_post(self):
        self.ensure_one()
        displayed_terms = []
        for term in self.document_term_ids:
            displayed_contents = []
            for content in term.content_ids:
                final_content = content.content
                for input_field in term.input_field_ids:  # Iterate through input fields for the current term
                    placeholder = "#(" + input_field.name + ")"
                    if placeholder in final_content:
                        final_content = final_content.replace(placeholder, input_field.value or "")  # Handle potential missing values
                displayed_contents.append((0, 0, {'content': final_content}))
            displayed_terms.append((0, 0, {'name': term.name, 'content_ids': displayed_contents}))
  
        self.document_term_display_ids = displayed_terms
        return self.write({'state': 'posted'})

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


class User(models.Model):
    _inherit = "res.users"

    document_ids = fields.One2many('contract.document', 'sideA_user_id', string="Documents", domain=[('status', 'not in', ['new', 'canceled'])],readonly=True)


    