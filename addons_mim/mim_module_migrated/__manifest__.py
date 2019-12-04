# -*- coding: utf-8 -*-
{
    'name': "mim_module_migrated",

    'version': '2.0',

    'description': """
    """,

    'author': "Lido",
    'sequence':1,
    'website': 'http://mim-madagascar.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    # any module necessary for this one to work correctly
    'depends': ['sale','sale_management','sale_crm','crm','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_view.xml',
        'views/mim_module_view.xml',
        'data/article.categorie.csv',
        'data/mim.article.csv',
        'report/sale_report_mim.xml',
        'views/stock_mim_view_move_picking.xml',
        'views/contre_mesure_view.xml',
        'views/crm_lead_view.xml',
        'views/company_view.xml',
    ],
    # only loaded in demonstration mode
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
    'css': ['static/src/css/css.css',],
    'icon':"mim_module/static/src/img/icon.png",
}