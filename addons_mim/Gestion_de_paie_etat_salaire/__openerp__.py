{
    'name': 'Gestion de la Paie - Etat global des salaires',
    'category': 'Localization/Payroll',
    'author': 'Ingenosya',
    'version': '1.0',
    'depends': ['hr_payroll','hr_contract','Gestion_de_paie'],
    'sequence':1,
	
    'description': """Ce module affiche tous les etats globales des salaires du module de Gestion de paie""",
    'data': [
        'ostie_view.xml',
        'etat_salaire_view.xml',
        'irsa_view.xml',
        'cnaps_view.xml',
        'report.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
