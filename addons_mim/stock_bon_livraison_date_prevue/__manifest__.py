# -*- coding: utf-8 -*-
{
    'name': "stock_bon_livraison_date_prevue",

    'summary': """
        stock_bon_livraison_date_prevue""",

    'description': """
        stock_bon_livraison_date_prevue
    """,

    'author': "MIM",
    'website': "http://www.mim-madagascar.com",

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
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

     'test':[],
    'installable':True,
    'application':True,
    'images':[],
    'icon': "mim_module/static/src/img/icon.png",

}