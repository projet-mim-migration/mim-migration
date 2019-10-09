# -*- coding: utf-8 -*-
{

    'name':'Gestion des reclamations/Ajout impression, workflow',
    'version':'0.1',
    'description':""" Prérequis :
            \n * module Vente installé
            \n * module crm_claim installé
            \n * Assignation des utilisateurs aux groupes : Groupe confirmer reclamation, Groupe mettre en cours reclamation, Groupe resoudre reclamation.\n Ce module permet de :
            \n * ajouter un nouveau etat Attente d\'affectation dans Ventes/After-Sale Services/Réclamations
            \n * ajouter un workflow à l\'objet crm_claim
            \n * imprimer la fiche de réclamations.
	    """,
    'sequence':1,
    'author':'Ando Nandrianina',
    'website':'http://mim-madagascar.com',
    'depends':['crm_claim'],
    'data':[
    'report/crm_claim.py',
    'crm_claim.py',
    'crm_claim_view.xml',
    'workflow_crm_claim.xml',
    'crm_claim_report.xml',
	],
    'test':[],
    'installable':True,
    'application':True,
    #'icon':"/stock_bon_de_livraison1/static/src/img/icon.png",
    'images':[],

} 
