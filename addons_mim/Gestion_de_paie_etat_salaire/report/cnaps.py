#-*- coding:utf-8 -*-

from odoo import models, api

class Cnaps(models.AbstractModel):
    _name = 'report.gestion_de_paie_etat_salaire.report_cnaps3_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        return{
            'doc_ids': docids,
            'doc_model': 'cnaps2',
            'docs': self.env['cnaps2'].browse(docids),
            'get_cnaps':self._get_cnaps,
            'get_plafond_cnaps':self._get_plafond_cnaps,
            'get_date_start_filter': self._get_date_start_filter,
            'get_date_end_filter': self._get_date_end_filter,
        }

    def _get_cnaps(self):
        sql="""SELECT c.date_from,c.date_to,c.num_emp,c.num_cin,e.num_cnaps_emp,
            c.name_related,c.basic,c.cnaps,c.cnapsemp,c.totalcnaps,c.brut,c.net 
            FROM cnaps2 c INNER JOIN hr_employee e ON c.employee_id=e.id
            WHERE c.date_from >= (SELECT date_start_filter FROM filter_cnaps)
            AND c.date_to <= (SELECT date_end_filter FROM filter_cnaps)
            AND c.id"""
        
        if len(self._ids)>1 :
            ids=tuple(self._ids)
            sql = sql + " IN {0}".format(ids)
        else :
            id = self._ids[0]
            sql = sql + " = {0}".format(id)
            
        self._cr.execute(sql)
        res=self._cr.dictfetchall()
        return res

    def _get_plafond_cnaps(self):
        sql = "SELECT res_company.plafond_cnaps FROM hr_payslip INNER JOIN res_company ON hr_payslip.company_id = res_company.id"
        self._cr.execute(sql)
        res = self._cr.fetchall()
        return res[0][0]
    
    def _get_date_start_filter(self):
        sql = "SELECT date_start_filter FROM filter_cnaps"
        self._cr.execute(sql)
        res = self._cr.fetchall()
        return res[0][0]
    
    def _get_date_end_filter(self):
        sql = "select date_end_filter from filter_cnaps"
        self._cr.execute(sql)
        res = self._cr.fetchall()
        return res[0][0]
    