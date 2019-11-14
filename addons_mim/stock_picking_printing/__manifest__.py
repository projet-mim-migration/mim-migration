# -*- coding: utf-8 -*-
{
    'name': "stock_picking_printing",

    'summary': """
        Impression bons de livraisons""",

    'description': """
        Ce module ajoute une nouvelle impression \'Suivi contre mesure et pose\' dans le sous menu Ventes/Bons de livraisons, objet : stock.picking.out
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
         'views/stock_view.xml',
        'report/rapport_stock.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
    'icon': "mim_module/static/src/img/icon.png",
}