# -*- coding: utf-8 -*-
{
    'name': "Tableau de bord",

    'summary': u"""
        Création tableau de bord
        """,

    'description': u"""
        Création de tableau de bord, l'utilisateur doit choisir:
            - 'Choix mois fin' si cochée permet de choisir mois fin,sinon mois fin = mois courant
            - 'A afficher' pour choisir quoi afficher dans le dashboard
            - 'Mesures' visible si 'vue graphique' cochée permet de choisir l'ordonnée du vue graphe entre 'montant' et 'nombre bde commande'
            - 'Dernier mois' visible si 'choix mois fin' cochée,permet de choisir jusqu'à quel mois filtrer les données
            - 'Année debut' pour le choix de l'année début auquel commencera le filtrage des données
            - 'Année fin' pour le choix de l'année fin auquel finira le filtrage des données 
            - 'Vue graphique' si cochée affiche le dashboard en mode graph, sinon le dashboard sera en mode list
            - 'Ajouter au tableau de bord' si cochée ajoute le filtre au tableau de bord,sinon le tableau de bord sera affichée mais ne sera pas sauvegardée
            - 'Nom tableau de bord' pour le nom du tableau de bord
            -  l'utilisateur doit choisir le dashboard dans lequel le filtre sera enregistrée
    """,

    'author': "Ingenosya Madagascar",
    'website': "http://www.ingenosya.mg",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_board.xml'],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'application':True,
}