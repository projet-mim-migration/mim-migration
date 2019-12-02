# -*- coding: utf-8 -*-
{
    'name':'Stock mim',
    'version':'0.1',
    'description':"""
        """,
    'author':'Lido',
    'website':'http://mim-madagascar.com',
    'depends':['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/stock_mim_view.xml',
        'views/stock_mim_view_move_picking.xml',
    ],
    'test':[],
    'installable':True,
    'images':[],
}