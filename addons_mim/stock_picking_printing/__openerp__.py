# -*- coding: utf-8 -*-
{

    'name':'Impression bons de livraisons',
    'version':'0.1',
    'description':"""Ce module ajoute une nouvelle impression \'Suivi contre mesure et pose\' dans le sous menu Ventes/Bons de livraisons, objet : stock.picking.out""",
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
