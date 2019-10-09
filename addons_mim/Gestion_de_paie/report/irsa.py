import time
from openerp.report import report_sxw

class irsa(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(irsa, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })
        
report_sxw.report_sxw('report.irsa', 'irsa','addons/Gestion_de_paie/report/irsa.rml', parser=irsa, header=True)