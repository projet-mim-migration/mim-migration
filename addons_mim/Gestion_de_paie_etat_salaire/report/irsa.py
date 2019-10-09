import time
from openerp.report import report_sxw

class irsa(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(irsa, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })
        
report_sxw.report_sxw('report.irsa2', 'irsa2','addons/Gestion_de_paie_etat_salaire/report/irsa.rml', parser=irsa, header=True)