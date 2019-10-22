# -*- coding: utf-8 -*-
{
    'name': "Gestion des reclamations/Ajout impression, workflow",

    'summary': """
    """,

    'description': """
        Prérequis :
            \n * module Vente installé
            \n * module bi_crm_claim installé
            \n * Assignation des utilisateurs aux groupes : Groupe confirmer reclamation, Groupe mettre en cours reclamation, Groupe resoudre reclamation.\n Ce module permet de :
            \n * ajouter un nouveau etat Attente d'affectation dans Ventes/After-Sale Services/Réclamations
            \n * ajouter un workflow à l'objet crm_claim
            \n * imprimer la fiche de réclamations.
    """,

    'sequence': 1,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'Uncategorized',
    'version': '2.0',

    'depends': ['bi_crm_claim'],

    'data': [
        'views/crm_claim_view.xml',
        # 'views/workflow_crm_claim.xml',
        'report/crm_claim_report.xml',
    ],

    'installable':True,
    'application':True,
}