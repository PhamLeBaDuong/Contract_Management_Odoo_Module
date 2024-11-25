{
    'name': "Contract Management",
    # The first 2 numbers are Odoo major version, the last 3 are x.y.z version of the module.
    'version' : "18.0.1.0.0",
    'depends' : ['base', 'base_setup'],
    'author' : 'Duong Pham',
    # Categories are freeform, for existing categories visit ...
    'category' : 'Customizations',
    'description' : """
    Module description
    """,
    # data files always loaded at installation
    'data': [        
        'security/ir.model.access.csv',
        # 'views/estate_property_views.xml',
        # 'views/estate_property_type_views.xml',
        # 'views/estate_property_tag_views.xml',
        # 'views/estate_property_offer_views.xml',
        # 'views/estate_menus.xml'
    ],
    "application" : False,
    "installable" : True,
    "auto_install" : False,
    "license" : "Other proprietary",
}