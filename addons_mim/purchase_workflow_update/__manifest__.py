# -*- coding: utf-8 -*-
{
    'name': "Modification Workflow purchase",

    'summary': """
    """,

    'description': """
        Ce module permet de sauter l'état 'confirmed' du workflow 'Purchase Order Basic Workflow' 
    de l'objet 'purchase.order' si les lignes de lignes d'achats correspondent a une categorie designee pour les Services par exemple. 
    Il permet egalement de tester dans la creation de facture si une piece jointe a été ajoutée dans une facture. Modules requises : purchase, document, account. 
    Il faut aussi ajouter la fonction 'invoice_validate2()'' dans l'activite open du workflow 'account.invoice.basic'.
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",


    'category': 'Uncategorized',
    'version': '2.0',

    'depends': ['purchase','product','account'],

    'data': [
        'security/purchase_order_security.xml',
        'views/product_view.xml',
        'views/purchase_view.xml',
    ],

    'installable':True,
    'application':True,
}