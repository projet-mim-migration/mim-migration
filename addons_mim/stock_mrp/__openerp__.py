# -*- coding: utf-8 -*-

{
 'name': 'Split picking, Generate manufacturing order',
 'description': """Ce module permet de diviser un bon de livraison sans avoir de lignes de mouvement de stock à l'état 'Disponible'. 
 Il permet également de créer tous les ordres de fabrication correspondant à chapue mouvement de stock rattaché à un bon de livraison""",
 'author': 'Ingenosya',
 'version': '8.0',
 'category': 'Gestion de stock',
 'depends': ['stock', 'mrp'],
 'website': 'http://www.ingenosya.com',
 'data': ['stock_view.xml','stock_split_details.xml','date_planned_view.xml',],
 'demo': [],
 'installable': True,
 'auto_install': False,
 }
