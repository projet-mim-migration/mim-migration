# -*- coding: utf-8 -*-
{
    'name': 'Mim module-Add image',
    'version': '1.0',
    'description': """ Ce module permet d\'ajouter une image dans Ventes/Bons de commande ou Devis/Ajout avance. Des qu\'une modification est effectuee dans votre devis (Mim wizard) l\'image change instantanement en fonction du choix effectue   
	""",
    'author': 'Ando',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['sale'],
    'data': [
	    'mim_module.py',
        'mim_module_view.xml',
        'sale_report.xml',
        'sale_view.xml',
        #'res_currency_view.xml',
            ],
    'css': ['static/src/css/css.css',],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
