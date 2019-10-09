# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class sale_order(osv.osv):
    _inherit = "sale.order"

    _columns = {
        'to_cancel' : fields.boolean('A annuler')
        }
    _defaults = {
        'to_cancel' : False,
    }

    # def onchange_to_cancel(self, cr, uid, ids, to_cancel, context=None):
    #     order_obj = self.pool.get('sale.order')
    #     order_obj.write(cr, uid, ids, {'to_cancel': to_cancel}, context=context)
    #     return {'value': {'to_cancel': to_cancel,}}

    def action_button_confirm2(self):
        sale_delete_form_id = self.env['ir.model.data'].get_object_reference('crm_lead', 'sale_order_delete_wizard_form')[1]
        ctx = dict()
        
        order_obj = self.env['sale.order']
        order = order_obj.browse()
        order_to_delete_ids = order_obj.search([('partner_id', '=', order.partner_id.id), ('state', 'in', ('draft', 'sent')), ('user_id', '=', order.user_id.id), ('id', '!=', self.env.ids[0])]) 
        order_obj.write(order_to_delete_ids, {'to_cancel': False})
        
        ctx['source_id'] = self.env.ids[0]
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.delete',
            'views': [(sale_delete_form_id, 'form')],
            'view_id': sale_delete_form_id,
            'target': 'new',
            'context': ctx,
        }

    def unlink(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('sale.order')
        sale_orders = self.browse(cr, uid, ids, context=context)
        unlink_ids = []
        for s in sale_orders:
            if s.state in ['draft', 'cancel']:
                unlink_ids.append(s.id)
            elif s.state in ['sent']:
                order_obj.action_cancel(cr, uid, [s.id], context=context)
                unlink_ids.append(s.id)
            else:
                raise osv.except_osv(_('Invalid Action!'), _('In order to delete a confirmed sales order, you must cancel it before!'))

        return super(sale_order, self).unlink(cr, uid, unlink_ids, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        default = dict(context or {})
        order_obj = self.pool.get('sale.order')
        order = self.browse(cr, uid, id, context=context)
        if order.state in ['draft', 'sent']:
            order_obj.action_cancel(cr, uid, [id], context=context)
        return super(sale_order, self).copy(cr, uid, id, default, context=context)

    def check_uncheck(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_form')
        view_id = view_ref and view_ref[1] or False,

        order_obj = self.pool.get('sale.order')
        order = order_obj.browse(cr, uid, ids[0], context=context)
        # order_ids = order_obj.search(cr, uid, [('partner_id', '=', order.partner_id.id), ('state', 'in', ('draft', 'sent')), ('user_id', '=', order.user_id.id), ('id', '!=', ids[0])])
        # for id in order_ids:
        #     order_obj.write(cr, uid, [id], {'to_cancel': False}, context=context)
        
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Sales Order',
        #     'res_model': 'sale.order',
        #     'res_id': ids[0],
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'view_id': view_id,
        #     'target': 'new',
        #     # 'nodestroy': False,
        #     # 'key2': "client_action_multi",
        #     # 'multi': "True",
        # }
        
        order_obj.write(cr, uid, ids, {'to_cancel': not order.to_cancel}, context=context)
        
        sale_delete_form_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'crm_lead', 'sale_order_delete_wizard_form')[1]
        ctx = dict()
        ctx['source_id'] = context.get('source_id', False)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.delete',
            'views': [(sale_delete_form_id, 'form')],
            'view_id': sale_delete_form_id,
            'target': 'new',
            'context': ctx,
        }

    