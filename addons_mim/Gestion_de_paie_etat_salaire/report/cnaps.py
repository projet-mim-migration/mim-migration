#-*- coding:utf-8 -*-

from openerp.report import report_sxw

class cnaps(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(cnaps, self).__init__(cr, uid, name, context)
        self.localcontext.update({
                                    'get_cnaps':self.get_cnaps,
                                    'get_plafond_cnaps':self.get_plafond_cnaps,
                                    'get_date_start_filter': self.get_date_start_filter,
                                    'get_date_end_filter': self.get_date_end_filter,
                                })

    def get_cnaps(self):
        sql="""SELECT c.date_from,c.date_to,c.num_emp,c.num_cin,e.num_cnaps_emp,
            c.name_related,c.basic,c.cnaps,c.cnapsemp,c.totalcnaps,c.brut,c.net 
            FROM cnaps2 c INNER JOIN hr_employee e ON c.employee_id=e.id
            WHERE c.date_from >= (SELECT date_start_filter FROM filter_cnaps)
            AND c.date_to <= (SELECT date_end_filter FROM filter_cnaps)
            AND c.id"""
        
        if len(self.ids)>1 :
            ids=tuple(self.ids)
            sql = sql + " IN {0}".format(ids)
        else :
            id = self.ids[0]
            sql = sql + " = {0}".format(id)
            
        self.cr.execute(sql)
        res=self.cr.dictfetchall()
        return res

    def get_plafond_cnaps(self):
        sql = "SELECT res_company.plafond_cnaps FROM hr_payslip INNER JOIN res_company ON hr_payslip.company_id = res_company.id"
        self.cr.execute(sql)
        res = self.cr.fetchall()
        return res[0][0]
    
    def get_date_start_filter(self):
        sql = "SELECT date_start_filter FROM filter_cnaps"
        self.cr.execute(sql)
        res = self.cr.fetchall()
        return res[0][0]
    
    def get_date_end_filter(self):
        sql = "select date_end_filter from filter_cnaps"
        self.cr.execute(sql)
        res = self.cr.fetchall()
        return res[0][0]
    
report_sxw.report_sxw('report.cnaps3', 'cnaps2', 'addons/Gestion_de_paie_etat_salaire/report/cnaps.rml', parser=cnaps, header=True)