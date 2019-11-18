# -*- coding: utf-8 -*-
{
    'name': "stock_bon_livraison_final1",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MIM",
    'website': "http://www.mim-madagascar.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',        
        #'views/templates.xml',
        #'views/stock_picking_out_view_form.xml'
        'views/stock_view_form.xml',
        'views/stock_view_tree.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    #'icon':"/stock_bon_de_livraison1/static/src/img/icon.png",
    'images': [],
    'icon': "mim_module/static/src/img/icon.png",
}