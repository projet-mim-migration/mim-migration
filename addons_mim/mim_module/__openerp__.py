# -*- coding: utf-8 -*-
{
    'name': 'Mim module',
    'version': '2.0',
    'description': """
	""",
    'author': 'Lido',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['sale'],
    'data': [
	    'mim_module.py',
            'mim_module_view.xml',
            'sale_view.xml',
	    'article.categorie.csv',
            'mim.article.csv',
            ],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
    'icon':"mim_module/static/src/img/icon.png",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
