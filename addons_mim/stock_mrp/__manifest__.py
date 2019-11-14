# -*- coding: utf-8 -*-
{
    'name': "stock_mrp",

    'summary': """
        Split picking, Generate manufacturing order""",

    'description': """
        Ce module permet de diviser un bon de livraison sans avoir de lignes de mouvement de stock à l'état 'Disponible'. 
 Il permet également de créer tous les ordres de fabrication correspondant à chapue mouvement de stock rattaché à un bon de livraison
    """,

    'author': "MIM",
    'website': "http://www.mim-madagascar.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'views/stock_view.xml',
        'views/stock_split_details.xml',
        'views/date_planned_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
     'auto_install': False,
     'auto_install': False,
     'icon': "mim_module/static/src/img/icon.png",
}