# -*- coding: utf-8 -*-
{
    'name': 'CRM - Lead',
    'version': '1.0',
    'description': 'CRM - Lead',
    'author': 'Ingenosya Madagascar',
    'sequence':1,
    'website': 'www.ingenosya.com',
    'depends': ['crm', 'sale', 'stock', 'mim_module'],
    'data': [
	    'crm_lead_view.xml',
        'views/sale.xml',
        'views/stock.xml',
        ],
    'installable': True,
    'application':True,
}
