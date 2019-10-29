# -*- coding: utf-8 -*-
{
    'name': "Gestion de la Paie - Etat global des salaires",

    'summary': """
    """,

    'description': """
        Ce module affiche tous les etats globales des salaires du module de Gestion de paie
    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'sequence':1,

    'category': 'Localization/Payroll',
    'version': '2.0',

    'depends': ['hr_payroll','hr_contract','Gestion_de_paie'],

    'data': [
        'views/ostie_view.xml',
        'views/etat_salaire_view.xml',
        'views/irsa_view.xml',
        'views/cnaps_view.xml',
        'views/report.xml',
        'report/report_ostie.xml',
        'report/report_irsa2.xml',
        'report/report_cnaps3.xml',
    ],

    'installable': True,
    'application': False,
}