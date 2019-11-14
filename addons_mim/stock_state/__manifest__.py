# -*- coding: utf-8 -*-
{
    'name': "stock_state",

    'summary': """
       Ce module permet d\'ajouter un nouveau sous-menu Avancement de production dans le menu Entrepot/Recevoir-livrer des articles/ et d\'inserer les colonnes Attente de disponibilité, Contre mesure, Fiche de debit pour compter le nombre de produits situe dans chaque etat correspondant. Pour actualiser le tableau, il faut cliquer sur le bonton bleu en forme de petite fleche""",

    'description': """
        Ce module permet d\'ajouter un nouveau sous-menu Avancement de production dans le menu Entrepot/Recevoir-livrer des articles/ et d\'inserer les colonnes Attente de disponibilité, Contre mesure, Fiche de debit pour compter le nombre de produits situe dans chaque etat correspondant. Pour actualiser le tableau, il faut cliquer sur le bonton bleu en forme de petite fleche
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
        'views/stock_view.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
    'icon': "mim_module/static/src/img/icon.png",

}