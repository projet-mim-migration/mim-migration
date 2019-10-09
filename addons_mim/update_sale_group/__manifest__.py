# -*- coding: utf-8 -*-
{
    'name': "Update sale group",

    'summary': """
    """,

    'description': """
        Module pour mettre readonly la colonne 'price_unit' du module sale pour un ou plusieurs groupes. 
        A installer avant l'installation du module update_sale 
        et il faut assigner les utilisateurs dans le groupe : Ventes
    """,

    'author': "INGENOSYA",
    'website': "http://mim-madagascar.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['sale'],

    'data': [
        'views/sale_order_view2.xml',
    ],

    'installable':True,
    'application':True,

    'icon':"/update_sale_group/static/src/img/icon.png",
}