# -*- coding: utf-8 -*-
{
    'name': "MIM - Vente",

    'summary': """
        Vente d'un article avancé
    """,

    'version': '2.0',

    'description': """
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Sales',
    'version': '2.0',
    'sequence': 1,

    'depends': [
        'sale',
        'sale_management',
        'sale_crm',
        'crm',
        'stock'
    ],

    'data': [
        'security/ir.model.access.csv',
        'security/mim_sale_group.xml',
        'data/article.categorie.csv',
        'data/mim.article.csv',
        'views/sale_view.xml',
        'views/mim_module_view.xml',
        'views/stock_mim_view_move_picking.xml',
        'views/contre_mesure_view.xml',
        'views/company_view.xml',
        'views/sale_delete_view.xml',
        'report/sale_report_mim.xml',
    ],

    'application':True,
    'css': ['static/src/css/css.css',],
}