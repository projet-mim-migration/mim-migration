# -*- coding: utf-8 -*-
{
    'name':'stock_mim_migrated',
    'version':'0.1',
    'description':"""
        """,
    'author':'Lido',
    'website':'http://mim-madagascar.com',
    'depends':['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_move_view.xml',
        'views/stock_report.xml',
        'views/stock_view_tree.xml',
        'views/stock_view_form.xml',
        'views/stock_mim_view_move_picking.xml',
        'report/rapport_stock.xml',
    ],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
    'icon': "mim_module/static/src/img/icon.png",
}