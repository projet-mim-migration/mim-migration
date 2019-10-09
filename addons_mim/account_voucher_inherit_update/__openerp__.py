# -*- coding: utf-8 -*-
{

    'name':'Modification Comptabilite/Paiements client /ajout mise a jour',
    'version':'0.1',
    'description':""" A installer après l'installation du module account_voucher_inherit   
	    """,
    'sequence':1,
    'author':'Ando Nandrianina',
    'website':'http://mim-madagascar.com',
    'depends':['sale','sale_crm'],
    'data':[
            'view_sale_advance_payment_inv.xml',
	],
    'test':[],
    'installable':True,
    'application':True,
    'images':[],

} 
