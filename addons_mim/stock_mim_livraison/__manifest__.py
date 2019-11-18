# -*- coding: utf-8 -*-
{
    'name': "stock_mim_livraison",

    'summary': """
        stock_mim_livraison""",

    'description': """
       Ce module ajoute une restriction au bouton \'Livraison\' dans le menu Entrepot/Recevoir/Livrer par commandes/Bons de livraison . Ce bouton est visible (en cliquant sur une ligne dans Bons de livraison) uniquement pour les utilisateurs inserer dans le groupe \'Utilisateur stock\' 
    """,

    'author': "MIM",
    'website': "http://www.mim-madagascar.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_mim_view.xml',
        'views/stock_mim_view2.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'test':[],
    'installable':True,
    'application':True,
    'icon':"/stock_mim_livraison/static/src/img/icon.png",
    'images':[],
    'icon': "mim_module/static/src/img/icon.png",

}