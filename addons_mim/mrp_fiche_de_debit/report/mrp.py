# -*- coding: utf-8 -*-

import time
from openerp.report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })
report_sxw.report_sxw('report.mrp.production.order2','mrp.production','addons/mrp_fiche_de_debit/report/order.rml',parser=order,header=False)