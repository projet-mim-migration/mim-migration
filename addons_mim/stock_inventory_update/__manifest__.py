# -*- coding: utf-8 -*-
{
    'name': "stock_inventory_update",
    'version': '0.1',
    'sequence': 1,
    'author': "Ingenosya",
    'website': "http://www.ingenosya.com",

    # Tous les autres modules nécessaires aux autre modules
    'depends': ['base', 'stock'],

    # Les fichiers chargés
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}