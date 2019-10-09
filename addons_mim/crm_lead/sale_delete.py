# -*- coding: utf-8 -*-

from openerp import models, api, fields
from openerp.exceptions import except_orm


class sale_order_delete(models.Model):
    _name = "sale.order.delete"

    name = fields.Char('Devis source')
    # order_ids = fields.One2many('sale.order', 'order_to_delete_id', string='Devis à supprimer')
    order_ids = fields.Many2many('sale.order', string='Devis à annuler')
    order_id = fields.Many2one('sale.order', string='Source')
    
    @api.model
    def default_get(self, vals):
    	res = super(sale_order_delete, self).default_get(vals)
    
    	order_obj = self.env['sale.order']
        source_id = self.env.context.get('source_id', False)
        if not source_id:
            raise except_orm('Erreur', 'L\'identifiant du devis source n\'a pas été récuperé')
        order = order_obj.browse(source_id)
        order_ids = order_obj.search([('partner_id', '=', order.partner_id.id), ('state', 'in', ('draft', 'sent')), ('user_id', '=', order.user_id.id), ('id', '!=', source_id)]) 
        order_to_delete_ids = []
        for o in order_ids:
            order_to_delete_ids.append(o.id)
        res.update({
            'name': order.name,
            'order_id': order.id,
            'order_ids': order_to_delete_ids,
        	})
        
        return res

    @api.v7
    def cancel_and_confirm(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('sale.order')
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ctx={}
        rec = self.browse(cr, uid, ids, context=context)[0]
        order_obj.action_button_confirm(cr, uid, [rec.order_id.id], context=context)
        for o in rec.order_ids:
            if o.to_cancel:
                order_obj.action_cancel(cr, uid, [o.id], context=context)
            # order_obj.write(cr, uid, [o.id], {'to_cancel': False}, context=context)
        
        return True

    @api.v7
    def confirm(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('sale.order')
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ctx={}
        rec = self.browse(cr, uid, ids, context=context)[0]
        order_obj.action_button_confirm(cr, uid, [rec.order_id.id], context=context)
        # for o in rec.order_ids:
        #     order_obj.write(cr, uid, [o.id], {'to_cancel': False}, context=context)
        
        return True



