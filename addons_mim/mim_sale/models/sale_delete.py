# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions


class SaleOrderDelete(models.Model):
	_name = "sale.order.delete"

	name = fields.Char('Devis source')
	order_ids = fields.Many2many('sale.order', string='Devis à annuler')
	order_id = fields.Many2one('sale.order', string='Source')
	
	@api.model
	def default_get(self, values):
		res = super(SaleOrderDelete, self).default_get(values)
	
		order_obj = self.env['sale.order']
		source_id = self.env.context.get('source_id', False)
		if not source_id:
			raise exceptions.UserError("L'identifiant du devis source n'a pas été récuperé")
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

	@api.multi
	def confirm(self):
		order_obj = self.env['sale.order']
		self.order_id.action_confirm()
		for o in self.order_ids :
			order_obj.search([('id','=',o.id)]).write({'to_cancel': False})
					
		return True

	@api.multi
	def cancel_and_confirm(self):
		order_obj = self.env['sale.order']
		self.order_id.action_confirm()
		
		for o in self.order_ids:
			if o.to_cancel:
				order_obj.search([('id','=',o.id)]).action_cancel()

		return True


class SaleOrder(models.Model):    
    _inherit = "sale.order"

    to_cancel = fields.Boolean('A annuler',default=False)
    

    def action_button_confirm2(self):
        sale_delete_form_id = self.env['ir.model.data'].get_object_reference('mim_sale', 'sale_order_delete_wizard_form')[1]
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
                raise exceptions.Warning('In order to delete a confirmed sales order, you must cancel it before!')

        return super(SaleOrder, self).unlink()

    def copy(self):
        default = dict(self.env.context or {})
        order_obj = self.env['sale.order']
        order = self.browse()
        if order.state in ['draft', 'sent']:
            order_obj.action_cancel([self.id])
        return super(SaleOrder, self).copy(default)

    def check_uncheck(self):
        if self.env.context == None:
            self.env.context = {}
        
        view_ref = self.env['ir.model.data'].get_object_reference('sale', 'view_order_form')
        view_id = view_ref and view_ref[1] or False,

        order_obj = self.env['sale.order']
        order = order_obj.browse(self.ids[0])
        
        order_obj.search([('id','=',self.ids)]).write({'to_cancel': not order.to_cancel})
        
        sale_delete_form_id = self.env['ir.model.data'].get_object_reference('mim_sale', 'sale_order_delete_wizard_form')[1]
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