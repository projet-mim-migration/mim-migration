# -*- coding: utf-8 -*-
{
    'name': "Mail notification",

    'summary': """
    """,

    'description': """
        Ce module ajoutent les bulles de notifications de messages venant des bons de livraisons
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'sequence':1,

    'category': 'Uncategorized',
    'version': '2.0',

    'depends': ['stock'],

    'data': [
        'views/stock_view.xml',
    ],

    'installable':True,
    'application':True,
}