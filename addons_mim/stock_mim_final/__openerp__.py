# -*- coding: utf-8 -*-
{

    'name':'Stock MIM final',
    'version':'0.1',
    'description':"""Ce module permet d'ajouter un workflow à l\'objet stock.move visible dans le menu Entrepot/Recevoir/livrer des articles/Livrer les articles, le module ajoute egalement les nouveaux etats Contre mesure et Fiche de debit.\n
    Après l\'installation du module, les utilisateurs doivent etre assigner a leur groupe respectif : Utilisteurs fiche debit (bouton Fiche debit), Utilisteurs contre mesure (bouton Contre mesure), Utilisteurs Rendre disponible (bouton Rendre disponible), Utilisteurs Traitement (bouton Traiter totalement)  
	    """,
    'sequence':1,
    'author':'Ando Nandrianina',
    'website':'http://mim-madagascar.com',
    'depends':['stock'],
    'data':[
	'stock_mim.py',
    'stock.py',
	'stock_mim_view.xml',
	'stock_mim_view_move_picking.xml',
    'workflow_session.xml',
    'stock_update_button.xml',
	],
    'test':[],
    'installable':True,
    'application':True,
    #'icon':"/stock_mim_test_workflow/static/src/img/icon.png",
    'images':[],

} 
