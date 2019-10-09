import time
from openerp.report import report_sxw

class ostie(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ostie, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })
        
report_sxw.report_sxw('report.ostie', 'ostie','addons/Gestion_de_paie_etat_salaire/report/ostie.rml', parser=ostie, header=True)