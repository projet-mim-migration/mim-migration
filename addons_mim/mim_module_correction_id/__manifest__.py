# -*- coding: utf-8 -*-
{
    'name': 'Mim module-Nomenclature',
    'version': '1.0',
    'description': """Les fonctions du module : 
            * Synchronise l\'id de sale.order.line avec celui de sale.order
            * Ajoute un multiplicateur valant 1.10 au total d'un devis dans mim wizard
            * Nomenclature des articles
             NB : ce module doit etre installer apres l\'installation des modules : mim_module et mim_module_add_image 
    """,
    'author': 'Ando',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['sale','stock','mim_module','mim_module_add_image'],
    

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_mim_view_move_picking.xml',
        'views/contre_mesure_view.xml',
    ],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
}