# -*- coding: utf-8 -*-
{
    'name': 'MRP - Fiche de débit',
    'version': '2.0',
    'description': """Ce module permet de creer un ordre de fabrication avancees en fonction du nombre, de la largeur et de la hauteur d\'un article. Ce module requiert l\'installation des modules suivants :\n
    * mrp
    * mim_module
    * stock
    """,
    'author': 'Ando',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['mrp','product'],
    'data': [
        'mrp.py',
        'mrp_view.xml',
        'product_product_view.xml',
        'stock_view.xml',
        'contre_mesure_view.xml',
        'mrp_report.xml',
        'mrp_workflow.xml',
        'choice_config_view.xml',
        'mrp_product_produce_view.xml',
            ],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
}
