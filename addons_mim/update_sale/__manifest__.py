# -*- coding: utf-8 -*-
{
    'name': "Update sale",

    'summary': """
    """,

    'description': """
        Module pour mettre readonly la colonne 'price_unit' du module sale. 
        A installer uniquement après l'installation du module 'update_sale_goup'
    """,

    'author': "INGENOSYA",
    'website': "www.ingenosya.com",

    'sequence': 1,
    'category': 'Uncategorized',
    'version': '2.0',

    'depends': ['sale'],

    'data': [
        'views/sale_order_view.xml',
    ],

    'installable':True,
    'application':True,

    'icon':"/update_sale/static/src/img/icon.png",
}