# -*- coding: utf-8 -*-
{
    'name': 'Mim module - Majoration de prix',

    'version': '1.0',
    'description': """ Majoration de prix""",
    'author': 'Ando',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['sale','base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_view.xml',
        'views/company_view.xml',
    ],
    'css': [],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
}
