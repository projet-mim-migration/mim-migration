# -*- coding: utf-8 -*-
{
    'name': 'Mim module Sale order',

    'version': '2.0',
    'description': """
    """,
    'author': 'Jims',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
    ],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
    'icon':"mim_module/static/src/img/icon.png",
}