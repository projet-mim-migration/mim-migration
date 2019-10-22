# -*- coding: utf-8 -*-
{
    'name':'Confirmed, Approved purchases',
    'vesion':'1.0',
    'description':" Ce module permet de gérer l\'affichage des boutons  \'Confirmer\' et \'Approuver\' une commade du module \'Achats\' (Purchases)",
    'author':'Ando Nandrianina RAZANAJATOVO',
    'sequence':1,
    # any module necessary for this one to work correctly
    'depends':['purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_view1.xml',
        'views/purchase_order_view2.xml',
        'views/purchase_order_view3.xml',
    ],
    
    'installable':True,
    'application':True,
    'icon':"/confirmed_approved/static/src/img/icon.png",
}
