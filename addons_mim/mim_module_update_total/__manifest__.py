# -*- coding: utf-8 -*-
{
    'name': 'Mim module-Update total',

    'version': '1.0',
    'description': """Ce module permet de mettre un mutliplicateur au total dans Devis/Ajout avance. NB : ce module doit etre installer apres l\'installation des modules mim_module et mim_module_add_image 
    """,
    'author': 'Ando',
    'sequence':1,
    'website': 'http://mim-madagascar.com',
    'depends': ['sale','mim_module','mim_module_add_image'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'test':[],
    'installable': True,
    'application':True,
    'images': [],
}