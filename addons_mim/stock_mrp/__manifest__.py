# -*- coding: utf-8 -*-
{
    'name': "Split picking, Generate manufacturing order",

    'summary': """
    """,

    'description': """
        Ce module permet de diviser un bon de livraison sans avoir de lignes de mouvement de stock à l'état 'Disponible'. 
        Il permet également de créer tous les ordres de fabrication correspondant à chapue mouvement de stock rattaché à un bon de livraison
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Inventory',
    'version': '2.0',

    'depends': ['stock', 'mrp'],

    'data': [
        'security/ir.model.access.csv',
        'views/mrp_configuration_view.xml',
        'views/stock_split_details_view.xml',
        'views/stock_view.xml',

    ],
}