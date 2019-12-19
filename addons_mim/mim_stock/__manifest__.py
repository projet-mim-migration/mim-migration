# -*- coding: utf-8 -*-
{
    'name': "MIM - Gestion de stock",

    'summary': """
        Gestion de stock avec création d'ordre de fabrication
    """,

    'description': """
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Inventory',
    'version': '2.0',
    'sequence': 1,

    'depends': [
        'mrp',
        'stock',
        'mim_sale',
        'mim_mrp'
    ],

   'data': [
        'security/ir.model.access.csv',
        'security/mim_stock_group.xml',
        'views/mrp_configuration_view.xml',
        'views/stock_move_view.xml',
        'views/stock_report.xml',
        'views/stock_view_tree.xml',
        'views/stock_view_form.xml',
        'views/stock_move_picking_view.xml',
        'views/stock_split_details_view.xml',
        'views/stock_view.xml',
        'report/rapport_stock.xml',
    ],

    'application': True
}