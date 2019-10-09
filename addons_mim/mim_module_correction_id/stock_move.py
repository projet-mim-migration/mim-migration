# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields

class stock_move (osv.osv):
    _inherit = 'stock.move'
    _columns = {
                'largeur': fields.float('Largeur'),
                'hauteur': fields.float('Hauteur'),
                }
    def edit_contre_mesure(self, cr, uid, ids, context=None):
        ctx = dict()
        ctx.update({
            'default_stock_move_id': self.browse(cr, uid, ids, context=context)[0].id
        })
        return {
            'name': 'Saisie Contre mesure',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contremesure',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }
stock_move()