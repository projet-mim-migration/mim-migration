# -*- coding: utf-8 -*-
{
    'name': "Modification Comptabilite/Paiements client /ajout mise a jour",

    'summary': """
    """,

    'description': """
        A installer après l'installation du module account_voucher_inherit
    """,

    'sequence': 1,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Uncategorized',
    'version': '2.0',

    'depends': ['sale', 'sale_crm'],

    'data': [
        'views/view_sale_advance_payment_inv.xml',
    ],

    'installable': True,
    'application': True,
}
