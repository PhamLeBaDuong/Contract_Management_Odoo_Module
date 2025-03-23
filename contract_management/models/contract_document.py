from datetime import timedelta
from odoo import Command, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class ContractDocument(models.Model):
    _name = "contract.document"
    _description = "Contract Document"

    title = fields.Char()
    
    sideA_user_id = fields.Many2one('res.users', string="Side A", index=True, tracking=True, required=True)
    # sideA_id = fields.Many2one(related='sideA_user_id.employee_id', string='Side A')
    sideA_name = fields.Char(string="Side A Name")
    sideA_birthday = fields.Date(string="Side A Birthday")
    sideA_work_email = fields.Char(string="Side A Work Email")
    sideA_work_phone = fields.Char(string= "Side A Work Phone")
    sideA_address_id = fields.Many2one('res.partner', string="Side A Address")
    sideA_signature = fields.Image()

    sideB_user_id = fields.Many2one('res.users', string="Side B", default = lambda self: self.env.user, index=True, tracking=True, readonly=True)
    sideB_id = fields.Many2one(related='sideB_user_id.employee_id', string='Side B')
    sideB_name = fields.Char(related='sideB_user_id.employee_id.name')
    sideB_birthday = fields.Date(related='sideB_user_id.employee_id.birthday')
    sideB_work_phone = fields.Char(related='sideB_user_id.work_phone')
    sideB_work_email = fields.Char(related='sideB_user_id.work_email')
    sideB_address_id = fields.Many2one(related='sideB_user_id.employee_id.address_id')
    sideB_signature = fields.Image()


    template_id = fields.Many2one('contract.template', string="Template")
    document_tag = fields.Many2many('contract.document.tag', string="Tag")
    date_of_creation = fields.Date('Date of Creation', default = fields.Date.today(), readonly=True)
    expiration_date = fields.Date('Expiration Date', default = fields.Date.today() + timedelta(days=365))
    date_of_execution = fields.Date('Date of Execution', readonly=True)
    version = fields.Integer()
    
    has_product = fields.Boolean(string="Has Product?", default=False)
    product_name = fields.Char(string="Product Name")
    product_price = fields.Float(string="Product Value")
    product_description = fields.Text(string="Product Description")
    product_quantity = fields.Integer(string="Product Quantity")
    # payment_term = fields.Selection(string="Payment Term", selection=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually'), ('one_time', 'One Time')], default='one_time')
    
    status = fields.Selection(string="Status", selection=[('new', 'New'), ('sent', 'Sent'), ('signed', 'Signed'), ('canceled', 'Canceled')], default='new')
    state = fields.Selection(string="State", selection=[('draft','Draft'), ('posted','Posted')], default='draft')

    document_term_ids = fields.Many2many('contract.term', string="Terms")
    # document_term_ids = fields.One2many('contract.term', 'document_id', string="Terms")
    input_fields_ids = fields.Many2many('contract.input.field', string="Input Fields")
    term_content_ids = fields.Many2many('contract.term.content', string="Contents")
    document_term_display_ids = fields.Many2many('contract.term.display', 'document_id', string="Terms", readonly=True)

    # @api.onchange('sideA_user_id')
    # def _onchange_sideA_id(self):
    #     if self.sideA_user_id:
    #         self.sideA_name = self.sideA_user_id.employee_id.name
    #         self.sideA_birthday = self.sideA_user_id.employee_id.birthday
    #         self.sideA_work_email = self.sideA_user_id.work_email
    #         self.sideA_work_phone = self.sideA_user_id.work_phone
    #         self.sideA_address_id = self.sideA_user_id.employee_id.address_id
    
    @api.onchange('sideA_user_id')
    def _onchange_sideA_id(self):
        if not self.sideA_user_id:
            return
            
        # Get user information directly from res.users and res.partner
        self.sideA_work_email = self.sideA_user_id.email
        self.sideA_work_phone = self.sideA_user_id.work_phone
        
        # Try to get employee info using sudo() to bypass security restrictions
        # This will only be used to populate the form fields, not to modify employee records
        if self.sideA_user_id.employee_id:
            employee = self.env['hr.employee'].sudo().browse(self.sideA_user_id.employee_id.id)
            if employee:
                self.sideA_birthday = employee.birthday
                self.sideA_address_id = employee.address_id
                self.sideA_name = employee.name
                # Only override email if available from employee
                # if employee.work_email:
                #     self.sideA_work_email = employee.work_email
    
    
    @api.onchange('template_id')
    def _fetch_fields(self):  
        self.ensure_one()
        if not self.template_id:
            return
        
        # # print('a')
        # if self.template_id:
        #     self.document_term_ids = [(5,0,0)]
        #     term_commands = []
        #     for term in self.template_id.term_ids:
        #         term_commands.append((0, 0, {
        #             'name': term.name,
        #             'input_field_ids': [(0, 0, {'name': x.name, 'field_type': x.field_type}) for x in term.input_field_ids],
        #             'content_ids': [(0, 0, {'content': x.content}) for x in term.content_ids],
        #             'description': term.description,
        #         }))
            
        #     self.document_term_ids = term_commands
        
        # Clear existing terms
        self.document_term_ids = [(5, 0, 0)]
        
        # Get the template terms
        template_terms = self.template_id.term_ids
        
        # Create new terms one by one
        for template_term in template_terms:
            # First create new input fields
            new_input_field_ids = []
            for field in template_term.input_field_ids:
                new_field = self.env['contract.input.field'].create({
                    'name': field.name,
                    'field_type': field.field_type, 
                })
                new_input_field_ids.append(new_field.id)
                
            # Then create new content records
            new_content_ids = []
            for content in template_term.content_ids:
                new_content = self.env['contract.term.content'].create({
                    'content': content.content,
                })
                new_content_ids.append(new_content.id)
            
            # Now create the term with links to the new fields and content
            new_term = self.env['contract.term'].create({
                'name': template_term.name,
                'description': template_term.description,
                'input_field_ids': [(6, 0, new_input_field_ids)],  # Replace with all new fields
                'content_ids': [(6, 0, new_content_ids)],  # Replace with all new content
            })
            
            # Link the new term to the document
            self.write({
                'document_term_ids': [(4, new_term.id)]
            })
        
        # Refresh the view
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
            
            # for term in self.template_id.term_ids:
            #     # fetch_input_fields = [(0, 0, {'name': x.name, 'field_type': x.field_type}) for x in term.input_field_ids]
            #     # fetch_content_fields = [(0, 0, {'content': x.content}) for x in term.content_ids]

            #     self.document_term_ids = [(0, 0, {
            #         'name': term.name,
            #         # 'input_field_ids':  [(4, x) for x in term.input_field_ids.ids],
            #         # 'content_ids': [(4, x) for x in term.content_ids.ids],
            #         # 'input_field_ids':  [(4, x) for x in fetch_input_fields.ids],
            #         # 'content_ids': [(4, x) for x in fetch_content_fields.ids],
            #     #     'input_field_ids': [(0, 0, {'name': x.name, 'field_type': x.field_type}) for x in term.input_field_ids] + 
            #     #    [(4, x.id, 0) for x in self.input_fields_ids],
            #     #     'content_ids': [(0, 0, {'content': x.content}) for x in term.content_ids] + 
            #     #    [(4, x.id, 0) for x in self.term_content_ids],
            #         'input_field_ids': [(0, 0, {'name': x.name, 'field_type': x.field_type}) for x in term.input_field_ids],
            #         'content_ids': [(0, 0, {'content': x.content}) for x in term.content_ids],
            #         'description': term.description,
            #     })]
            
        # else:
        #     self.document_term_ids = [(5,0,0)]
            
    def print_contract(self):
        self.ensure_one()
        return self.env.ref('contract_management.action_contract_document_report').report_action(self)
    
    def send_contract(self):
        self.ensure_one()
        if self.has_product:
            self.env['account.move'].create(
                {
                    'partner_id': self.sideA_user_id.partner_id.id, 
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            'name': self.product_name,
                            'price_unit': self.product_price,
                            'quantity': self.product_quantity
                        })
                    ]
                }
            )
        return self.write({'status': 'sent'})
    
    def sign_contract(self):
        self.ensure_one()
        return {
            'name': 'Confirm Signature',
            'type': 'ir.actions.act_window',
            'res_model': 'contract.signature.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('contract_management.contract_signature_wizard_view_form').id, 
            'target': 'new',
            'data': {'document_id': self.id},
            'context': {'default_document_id': self.id},
        }
            
    def signed(self):
        return
    
    def action_post(self):
        self.ensure_one()
        displayed_terms = []
        for term in self.document_term_ids:
            displayed_contents = []
            for content in term.content_ids:
                final_content = content.content
                for input_field in term.input_field_ids:
                    placeholder = "#(" + input_field.name + ")"
                    if placeholder in final_content:
                        final_content = final_content.replace(placeholder, input_field.value or "")
                displayed_contents.append((0, 0, {'content': final_content}))
            displayed_terms.append((0, 0, {'name': term.name, 'content_ids': displayed_contents}))
  
        self.document_term_display_ids = displayed_terms
        return self.write({'state': 'posted'})

class User(models.Model):
    _inherit = "res.users"

    document_ids = fields.One2many(
        'contract.document', 
        string="Documents", compute='_compute_document_ids'
    )

    @api.depends('document_ids.sideA_user_id', 'document_ids.sideB_user_id')
    def _compute_document_ids(self):
        for user in self:
            document_ids = self.env['contract.document'].search(
                ['|', ('sideA_user_id', '=', user.id), ('sideB_user_id', '=', user.id)]
            )
            user.document_ids = document_ids


    