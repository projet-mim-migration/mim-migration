# -*- coding: utf-8 -*-
{
    'name': "MRP - Fiche de débit",

    'summary': """
    """,

    'description': """
        Ce module permet de creer un ordre de fabrication avancees en fonction du nombre, de la largeur et de la hauteur d'un article. 
        Ce module requiert l'installation des modules suivants :\n
            * mrp
            * mim_module
            * stock
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Manufacturing',
    'version': '2.0',

    'depends': ['mrp','mim_module', 'stock', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'security/mrp_security.xml',
        'security/stock_security.xml',
        'views/choice_config_view.xml',
        # 'views/contremesure_view.xml',
        'views/mrp_bom_view.xml',
        'views/mrp_component_view.xml',
        # 'views/mrp_product_produce_view.xml',
        'views/mrp_production_view.xml',
        'views/product_product_view.xml',
        'views/stock_move_view.xml',
        'report/mrp_production_report_view.xml',
    ],
}