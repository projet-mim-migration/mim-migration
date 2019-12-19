# -*- coding: utf-8 -*-
{
    'name': "MIM - Gestion de fabrication",

    'summary': """
        Création d'un ordre de fabrication avancée d'un article
    """,

    'description': """
        Ce module permet de creer un ordre de fabrication avancees en fonction du nombre, de la largeur et de la hauteur d'un article. 
        Ce module requiert l'installation des modules suivants :\n
            * mrp
            * mim_sale
            * stock
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Manufacturing',
    'version': '2.0',
    'sequence': 1,

    'depends': [
        'mrp',
        'stock', 
        'product',
        'mim_sale'
    ],

    'data': [
        'security/ir.model.access.csv',
        'security/mrp_group.xml',
        'security/stock_group.xml',
        'views/choice_config_view.xml',
        'views/mrp_bom_view.xml',
        'views/mrp_component_view.xml',
        'views/mrp_production_view.xml',
        'views/product_product_view.xml',
        'views/stock_move_view.xml',
        'report/mrp_production_report_view.xml',
        'data/res_config_data.xml'
    ],

    'application': True
}