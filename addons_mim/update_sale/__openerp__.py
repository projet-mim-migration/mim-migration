# -*- encoding: utf-8 -*-
{
    'name':'Update sale ',
    'vesion':'1.0',
    'description':" Module pour mettre readonly la colonne 'price_unit' du module sale. A installer uniquement après l\'installation du module update_sale_goup ",
    'author':'Ando Nandrianina RAZANAJATOVO',
    'sequence':1,
    'data': [
          'sale_order_view.xml',
        ],
    'installable':True,
    'application':True,
    'depends':['sale'],
    'icon':"/update_sale/static/src/img/icon.png",
}