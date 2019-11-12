# -*- coding: utf-8 -*-
{
    'name': 'Mim module-Add image',

    'description': """ Ce module permet d\'ajouter une image dans Ventes/Bons de commande ou Devis/Ajout avance. Des qu\'une modification est effectuee dans votre devis (Mim wizard) l\'image change instantanement en fonction du choix effectue   
    """,

    'author': 'Ando',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['sale','mim_module'],
        # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # always loaded
    'data': [
        # 'security/ir.model.access.csv','views/sale_report.xml',
        'views/sale_views.xml',
        'views/mim_module_view.xml',
        'report/sale_report_mim.xml',
    ],
    'css': ['static/src/css/css.css',],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
}
