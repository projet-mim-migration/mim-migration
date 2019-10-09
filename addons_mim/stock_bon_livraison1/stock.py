# -*- coding: utf-8 -*-

import time
from openerp.osv import fields, osv

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    #_table = "stock.picking"
    _columns = {
                'motivation':fields.text('Motivation'),
                'date_changed':fields.boolean(u'Date changée'),
                'motivation':fields.text('Motivation'),
                }
    _defaults = {
                 'date_changed':False,
                 }
    
    
    #Evenement losrque la date de livraison est modifié
    def onchange_fields(self, cr, uid, ids, context=None):
        if len(ids)>0:
            return {'value':{'date_changed':True}}
        else: return {'value':{'date_changed':False}}
            
    def write(self, cr, uid, ids, vals, context=None):
        #picking_data = self.browse(cr, uid, ids, context=context)[0]
        user_obj = self.pool.get('res.users')
        #uids = user_obj.search(cr, uid, [('id','=',uid)], context=context)
        user = user_obj.browse(cr, uid, uid, context=context)
        
        if 'date_changed' in vals:
            if vals['date_changed']==True:
                if 'motivation' in vals:
                    if vals['motivation']:
                        vals2 = {
                                    'body':'<p>'+u''+vals['motivation']+'</p>',
                                    'model':'stock.picking',
                                    #'record_name':picking_data.name,
                                    'date':time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'author_id':user.partner_id.id,
                                    'res_id':ids[0],
                                    'type':'comment',
                                }
                        self.pool.get('mail.message').create(cr, uid, vals2, context=context)
                        vals['date_changed'] = False
                        vals['motivation'] = False
                    else:raise osv.except_osv(('Erreur'), (u'Veuillez saisir la motivation de votre modification'))
                else:raise osv.except_osv(('Erreur'), (u'Veuillez saisir la motivation de votre modification'))
        
        super(stock_picking, self).write(cr, uid, ids, vals, context=context)
        
        return True    
stock_picking()
