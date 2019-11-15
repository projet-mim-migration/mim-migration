# -*- coding: utf-8 -*-
{
    'name': "Migration Stock_quants",

    'summary': """Migrate Stock_quants""",

    'description': """
        Module necessaire pour generer automatiquement les stock_quants 
    """,

    'author': "mika",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Migration ',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/generation.xml',
        #'views/templates.xml',
    ],
    
}