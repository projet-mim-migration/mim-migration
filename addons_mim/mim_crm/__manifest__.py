# -*- coding: utf-8 -*-
{
    'name': "MIM - CRM Lead",

    'summary': """
        CRM Lead
    """,

    'description': """

    """,

    'author': "INGENOSYA",
    'website': "http://www.ingenosya.com",

    'category': 'CRM',
    'version': '2.0',
    'sequence': 1,

    'depends': [
        'crm',
        'sale', 
        'stock',
        'bi_crm_claim'
    ],

    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'report/crm_claim_report.xml',
    ],

    'application': True
}