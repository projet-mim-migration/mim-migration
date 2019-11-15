# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
# -*- coding: utf-8 -*-

class sale_order(models.Model):
    
    _inherit = "sale.order"

    
    to_cancel = fields.Boolean('A annuler',default=False)
    
    # def onchange_to_cancel(self, cr, uid, ids, to_cancel, context=None):
    #     order_obj = self.pool.get('sale.order')
    #     order_obj.write(cr, uid, ids, {'to_cancel': to_cancel}, context=context)
    #     return {'value': {'to_cancel': to_cancel,}}

    def action_button_confirm2(self):
        sale_delete_form_id = self.env['ir.model.data'].get_object_reference('crm_lead', 'sale_order_delete_wizard_form')[1]
        ctx = dict()
        
        order_obj = self.env['sale.order']
        order = order_obj.browse()
        order_to_delete_ids = order_obj.search([('partner_id', '=', order.partner_id.id), ('state', 'in', ('draft', 'sent')), ('user_id', '=', order.user_id.id), ('id', '!=', self.ids[0])]) 
        order_obj.search([('id','=',order_to_delete_ids.id)]).write({'to_cancel': False})
        ctx['source_id'] = self.ids[0]
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
        
    def unlink(self):
        order_obj = self.env['sale.order']
    
        for order in self:
            if order.state in ['draft', 'cancel']:
                pass
            elif order.state in ['sent']:
                order_obj.search([('id','=',order.id)]).action_cancel()
            else:
                raise exceptions.Warning(_('In order to delete a confirmed sales order, you must cancel it before!'))

        return super(sale_order, self).unlink()

    def copy(self):
        default = dict(self.env.context or {})
        order_obj = self.env['sale.order']
        order = self.browse()
        if order.state in ['draft', 'sent']:
            order_obj.action_cancel([self.id])
        return super(sale_order, self).copy(default)

    def check_uncheck(self):
        if self.env.context == None:
            self.env.context = {}
        
        view_ref = self.env['ir.model.data'].get_object_reference('sale', 'view_order_form')
        view_id = view_ref and view_ref[1] or False,

        order_obj = self.env['sale.order']
        order = order_obj.browse(self.ids[0])
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
        
        order_obj.search([('id','=',self.ids)]).write({'to_cancel': not order.to_cancel})
        
        sale_delete_form_id = self.env['ir.model.data'].get_object_reference('crm_lead', 'sale_order_delete_wizard_form')[1]
        ctx = dict()
        ctx['source_id'] = self.env.context.get('source_id', False)
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

    