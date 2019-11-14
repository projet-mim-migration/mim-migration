# -*- coding: utf-8 -*-
{
    'name': "stock_move_print",

    'summary': """
        stock_move_print""",

    'description': """
        stock_move_print
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
        'report/stock_move.xml',
        #'report/stock_move_reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'images': [],
    'icon': "mim_module/static/src/img/icon.png",
}