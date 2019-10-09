# -*- coding: utf-8 -*-

from openerp.osv import osv


class mrp_product_produce(osv.osv_memory):
    _inherit = "mrp.product.produce"
    
    
    def consume(self, cr, uid, ids, context=None):
        production_id = context.get('active_id', False)
        assert production_id, "Production Id should be specified in context as a Active ID."
        data = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('mrp.production').action_produce(cr, uid, production_id,
                            data.product_qty, 'consume', data, context=context)
        return {}
    
    def consume_produce(self, cr, uid, ids, context=None):
        production_id = context.get('active_id', False)
        state_move = self.pool.get('mrp.production').browse(cr, uid, [production_id], context=context)[0].move_prod_id.state
        if state_move in ('flowsheeting','assigned','done'):
            assert production_id, "Production Id should be specified in context as a Active ID."
            data = self.browse(cr, uid, ids[0], context=context)
            self.pool.get('mrp.production').action_produce(cr, uid, production_id,
                                data.product_qty, 'consume_produce', data, context=context)
        else:
            raise osv.except_osv(('Erreur'), (u'Le mouvement de stock lié à cet ordre de fabrication n\'est pas dans l\'état Fiche de débit, Veuillez d\'abord Consommer'))
        return {}
    
mrp_product_produce()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
