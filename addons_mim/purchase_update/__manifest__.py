# -*- coding: utf-8 -*-
{
    'name':'Personnalisation achats',
    'version':'0.1',
    'description':"",
    'sequence':1,
    'author':'Ingenosya',
    'website':'http://www.ingenosya.com',
    'depends':['purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_view.xml',
    ],
    'test':[],
    'installable':True,
    'application':True,
    'images':[],
}