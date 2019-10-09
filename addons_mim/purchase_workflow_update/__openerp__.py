# -*- coding: utf-8 -*-
{

    'name':'Modification Workflow purchase',
    'version':'0.1',
    'description':"""Ce module permet de sauter l\'etat \'confirmed\' du workflow \'Purchase Order Basic Workflow\' 
    de l\'objet purchase.order si les lignes de lignes d\'achats correspondent a une categorie designee pour les Services par exemple. 
    Il permet egalement de tester dans la creation de facture si une piece jointe a ete ajoute dans une facture. Modules requises : purchase, document, account. Il faut aussi ajouter la fonction invoice_validate2() dans l\'activite open du workflow account.invoice.basic.
        """,
    'sequence':1,
    'author':'Ando',
    'website':'http://mim-madagascar.com',
    'depends':['purchase','product','purchase_double_validation','account'],
    'data':[
            'purchase.py',
            'product_category.py',
            'account_invoice.py',
            'product_view.xml',
            'purchase_view.xml',
            #'account_invoice_workflow.xml',
    ],
    'test':[],
    'installable':True,
    'application':True,
    'images':[],

} 
