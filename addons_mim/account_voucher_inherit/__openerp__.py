# -*- coding: utf-8 -*-
{

    'name':'Modification Comptabilite/Paiements client',
    'version':'0.1',
    'description':"""Ce module permet d\'ajouter un menu \'Paiements client/Vendeur \' dans Comptabilite/Clients, ce menu affiche un tableau identique au menu Paiements client, sauf que dans le tableau que presente ce nouveau menu on a rajoute la colonne Vendeur et tout le tableau est en lecture seule  
	    """,
    'sequence':1,
    'author':'Ando Nandrianina',
    'website':'http://mim-madagascar.com',
    'depends':['account_voucher'],
    'data':[
    'invoice.py',
    'account_voucher.py',
    'account_voucher_view.xml',
	],
    'test':[],
    'installable':True,
    'application':True,
    'images':[],

} 
