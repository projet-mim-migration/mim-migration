# -*- coding: utf-8 -*-
{

    'name':'Stock MIM livraison',
    'version':'0.1',
    'description':""" Ce module ajoute une restriction au bouton \'Livraison\' dans le menu Entrepot/Recevoir/Livrer par commandes/Bons de livraison . Ce bouton est visible (en cliquant sur une ligne dans Bons de livraison) uniquement pour les utilisateurs inserer dans le groupe \'Utilisateur stock\' 
	    """,
    'author':'Ando Nandrianina',
    'website':'http://mim-madagascar.com',
    'depends':['stock'],
    'data':[
	'stock_mim_view.xml',
    #'stock_mim_view2.xml',
	],
    'test':[],
    'installable':True,
    'application':True,
    'icon':"/stock_mim_livraison/static/src/img/icon.png",
    'images':[],

} 
