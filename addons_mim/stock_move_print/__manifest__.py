# -*- coding: utf-8 -*-
{
    'name': "Impression Mouvements de stock",

    'summary': """
    """,

    'description': """
        Impression Mouvements de stock
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Inventory',
    'version': '2.0',

    'depends': ['stock'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_view.xml',
        'report/report_stock_move.xml',
        #'report/stock_move_reports.xml',
    ],
}