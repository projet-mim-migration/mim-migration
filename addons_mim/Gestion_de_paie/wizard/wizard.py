from openerp.osv import osv, fields
import time

class filter_cnaps(osv.osv):
    _name = "filter_cnaps"
    _columns = {
        'date_start_filter': fields.date("Start Date"),
        'date_end_filter': fields.date("End Date"),
       # 'filter': fields.selection([('filter_no', 'No Filters'), ('filter_date', 'Date')], "Filter by", required=True),

    }
    
    _defaults = {
            'date_start_filter': lambda *a: time.strftime('%Y-01-01'),
            'date_end_filter': lambda *a: time.strftime('%Y-%m-%d'),
    }
   
    def onchange_filter(self, cr, uid, ids,filte='filter_no', context=None):
        res={'value':{}}
        if filte =='filter_no':
            res['value'] = {'date_start_filter': False ,'date_end_filter': False}

        if filte == 'filter_date':
            res['value'] = {'date_start_filter': time.strftime('%Y-01-01'), 'date_end_filter': time.strftime('%Y-%m-%d')}
        return res

    def check(self, cr, uid, ids, context=None):
        #=======================================================================
        # if context is None:
        #     context = {}
        # data = {}
        # data['ids'] = context.get('active_ids', [])
        # data['model'] = context.get('active_model', 'ir.ui.menu')
        # data['form'] = self.read(cr, uid, ids, ['date_start_filter', 'date_end_filter'], context)
        # res = self.read(cr, uid, data, context)
        # return res
        #=======================================================================
        
        cnaps_obj = self.pool.get('filter_cnaps')
        data = self.browse(cr, uid, ids, context)[0]
        old_cnaps_ids = cnaps_obj.search(cr, uid, [('id','!=',data.id)], context=context)
        cnaps_obj.unlink(cr, uid, old_cnaps_ids, context=context)
        
        return True
        
filter_cnaps()