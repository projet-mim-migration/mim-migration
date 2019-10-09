# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

    
class crm_claim(osv.osv):
    _inherit = "crm.claim"
    _columns = {
                'stage_id': fields.many2one ('crm.claim.stage', 'Stage', track_visibility='onchange',
                domain="['|', ('section_ids', '=', section_id), ('case_default', '=', True)]"),
                }
    _defaults = {
                 'stage_id':1,
                 }
    
    def action_set_to_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'stage_id': 1})
        return True
    
    def action_confirm(self, cr, uid, ids, context=None):
        id = self.pool.get('ir.model.data').get_object_reference(cr, uid,'crm_claim_inherit', 'stage_claim4')
        stage_id=id[1]
        self.write(cr, uid, ids, {'stage_id': stage_id})
        return True
        
    def action_open(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'stage_id': 2})
        return True
        
    def action_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'stage_id': 3})
        return True
    
    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'stage_id': 4})
        return True
    
crm_claim()