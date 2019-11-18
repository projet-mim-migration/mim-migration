# -*- coding: utf-8 -*-
{
    'name': "stock_mim_final",

    'summary': """
        stock_mim_final""",

    'description': """
        Ce module permet d'ajouter un workflow à l\'objet stock.move visible dans le menu Entrepot/Recevoir/livrer des articles/Livrer les articles, le module ajoute egalement les nouveaux etats Contre mesure et Fiche de debit.\n
    Après l\'installation du module, les utilisateurs doivent etre assigner a leur groupe respectif : Utilisteurs fiche debit (bouton Fiche debit), Utilisteurs contre mesure (bouton Contre mesure), Utilisteurs Rendre disponible (bouton Rendre disponible), Utilisteurs Traitement (bouton Traiter totalement)  
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
         #'views/stock_update_button.xml',
        'views/stock_mim_view_move_picking.xml',
         #'views/workflow_session.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

     'test':[],
    'installable': True,
    'application': True,
    'auto_install': False,
    #'icon':"/stock_mim_test_workflow/static/src/img/icon.png",
    'images':[],
    'icon': "mim_module/static/src/img/icon.png",

}