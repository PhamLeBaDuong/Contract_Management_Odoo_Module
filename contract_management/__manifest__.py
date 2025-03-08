{
    'name': "Contract Managementt",
    # The first 2 numbers are Odoo major version, the last 3 are x.y.z version of the module.
    'version' : "18.0.1.0.0",
    'depends' : ['base', 'base_setup','hr'],
    'author' : 'Duong Pham',
    # Categories are freeform, for existing categories visit ...
    'category' : 'Customizations',
    'description' : """
    Module descriptionnn
    """,
    # data files always loaded at installation
    'data': [        
        'security/ir.model.access.csv',
        'views/contract_document_views.xml',
        'views/contract_template_views.xml',
        'views/contract_document_tag.xml',
        'views/contract_term_views.xml',
        'views/contract_input_field_views.xml',
        'views/contract_term_content_views.xml',
        'views/contract_document_report.xml',
        'views/res_user_views.xml',
        'views/contract_signature_wizard_views.xml',
        'views/contract_menu.xml',
        'data/contract_template_data.xml'
    ],
    'demo': [
        'data/contract_template_data.xml' 
    ],
    "application" : True,
    "installable" : True,
    "auto_install" : False,
    "license" : "Other proprietary",
}