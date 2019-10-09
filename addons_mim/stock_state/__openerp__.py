# -*- coding: utf-8 -*-
{

    'name':'Stock state',
    'version':'0.1',
    'description':"""Ce module permet d\'ajouter un nouveau sous-menu Avancement de production dans le menu Entrepot/Recevoir-livrer des articles/ et d\'inserer les colonnes Attente de disponibilité, Contre mesure, Fiche de debit pour compter le nombre de produits situe dans chaque etat correspondant. Pour actualiser le tableau, il faut cliquer sur le bonton bleu en forme de petite fleche""",
    'sequence':1,
    'author':'Ando Nandrianina',
    'website':'http://mim-madagascar.com',
    'depends':['stock'],
    'data':[
    'stock_picking.py',
	'stock_view.xml',
	],
    'test':[],
    'installable':True,
    'application':True,
    'images':[],

} 
