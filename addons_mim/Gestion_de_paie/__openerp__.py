{
    'name': 'Madagascar - Gestion de la Paie',
    'category': 'Localization/Payroll',
    'author': 'MIM',
    'version': '1.0',
    'depends': ['hr_payroll','hr_contract'],
    'sequence':1,
	
    'description': """Madagascar Payroll Rules.
======================

   Gestion de la Paie Malgache:     
    - Gestion des employés.
    - Gestion des contrats.
    - Configuration et paramètrage
            * Les rubriques de paie :primes,indemnités,avantages,déductions,...
            * Les rubriques cotisable ,imposable , soumise à la prime d'ancienneté  ...
            * Les cotisations : cotisations salariales et patronales CNAPS,Mutuelle...
            * Barème de la prime d'ancienneté,cotisations CNAPS ...       
    - Calcul de paie selon les normes malagasy : calcul automatique de la prime d'ancienneté,heures supplémentaire,cotisations salariales et patronales,...
    - Gestion des congés  :Calcul automatique des congés non payés à partir du module hr_holidays
    - Comptabilisation de la paie :  configuration des comptes de credit et de débit
    - Reporting : les  bulletins de paie,journale de paie ,Ordres de virement ...
""",
    'active': False,
    'data': [
        'wizard/wizard.py',
        'view/gestion_de_paie_view.xml',
        'view/etat_salaire.xml',
        'view/cnaps.xml',
        'view/irsa.xml',
        'view/wizard.xml',
        'hr_contract_type.py',
        'hr_contract_type_view.xml',
        'gestion_de_paie_data.xml',
		
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
	

}
