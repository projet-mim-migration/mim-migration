# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields

class Contre_mesure (osv.osv):
    def _get_stock_move_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('stock_move_id', False)
    _name = 'contremesure'
    _columns = {
                'largeur': fields.float('Largeur'),
                'hauteur': fields.float('Hauteur'),
                'stock_move_id':fields.integer('Id current stock move line'),
                }
    _defaults = {
              'stock_move_id':_get_stock_move_id,
              }
    
    def update_contre_mesure(self, cr, uid, ids, context=None):
        stock_move_id = self.browse(cr, uid, ids, context=context)[0].stock_move_id
        self.pool.get('stock.move').write(cr, uid, [stock_move_id], {'largeur':self.browse(cr, uid, ids, context=context)[0].largeur,'hauteur': self.browse(cr, uid, ids, context=context)[0].hauteur})
        
Contre_mesure()