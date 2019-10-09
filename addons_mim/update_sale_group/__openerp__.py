# -*- encoding: utf-8 -*-
{
    'name':'Update sale group',
    'vesion':'1.0',
    'description':" Module pour mettre readonly la colonne 'price_unit' du module sale pour un ou plusieurs groupes. A installer avant l\'installation du module update_sale et il faut assigner les utilisateurs dans le groupe : Ventes",
    'author':'Ando Nandrianina RAZANAJATOVO',
    'sequence':1,
    'data': [
          'sale_order_view2.xml',
        ],
    'installable':True,
    'application':True,
    'depends':['sale'],
    'icon':"/update_sale_group/static/src/img/icon.png",
}