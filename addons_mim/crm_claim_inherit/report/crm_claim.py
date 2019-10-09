import time
from openerp.report import report_sxw

class claim(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(claim, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_selection_value': self._get_selection_value, 
            'test': self._testfunc,
        })
    def _get_selection_value(self, model, field, value):

        selection = self.pool.get(model)._columns.get(field).selection
        val = ''
        res = ''
        for v in selection:
            if v[0] == value:
                val = v[1]
                break
        if val == 'Highest':
            res = 'La plus haute' 
        if val == 'High':
            res = 'Haute'
        if val == 'Normal':
            res = 'Normale'
        if val == 'Low':
            res = 'Basse'
        if val == 'Lowest':
            res = 'La plus basse'
        return res
    
    def _testfunc(self):
        return "this the test text."
    
report_sxw.report_sxw('report.crm.claim', 'crm.claim','addons/crm_claim_inherit/report/claim.rml', parser=claim, header=True)