# -*- coding: utf-8 -*-
{
    'name': 'Mim module CRM LEAD',

    'version': '2.0',
    'description': """
    """,
    'author': 'Jims',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['sale_crm','crm','mim_module_sale_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
    ],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
    'icon':"mim_module/static/src/img/icon.png",
}
