# -*- encoding: utf-8 -*-
{
    'name':'Confirmed, Approved purchases',
    'vesion':'1.0',
    'description':" Ce module permet de gérer l\'affichage des boutons  \'Confirmer\' et \'Approuver\' une commade du module \'Achats\' (Purchases)",
    'author':'Ando Nandrianina RAZANAJATOVO',
    'sequence':1,
    'data': [
          'purchase_order_view1.xml','purchase_order_view2.xml','purchase_order_view3.xml',
        ],
    'installable':True,
    'application':True,
    'depends':['purchase'],
    'icon':"/confirmed_approved/static/src/img/icon.png",
}