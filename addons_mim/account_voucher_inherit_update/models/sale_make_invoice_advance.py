# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Invoice2(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _get_user_id(self):
        context = self._context or {}
        return context.get('user_id', False)
    
    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        readonly=True,
        default=_get_user_id,
        track_visibility='onchange',
        states={'draft':[('readonly',False)]}
    )


class SaleOrder(models.Model):
    
    _inherit = 'sale.order'

    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        states={
            'draft': [('readonly', False)], 
            'sent': [('readonly', False)]
        }, 
        select=True,
        track_visibility='onchange', 
        required=True,
        default=False,
    )

    categ_ids = fields.Many2many(
        'crm.case.categ', 
        'sale_order_category_rel', 
        'order_id', 
        'category_id', 
        'Tags',
        domain="['|', ('section_id', '=', section_id), ('section_id', '=', False), ('object_id.model', '=', 'crm.lead')]", 
        context="{'object_name': 'crm.lead'}", 
        required=True,
    )
 
    @api.multi
    def create_invoice_new(self):
        for inv in self:
            ctx = dict(self._context)
            
            self._context.update({
                'default_user_id':inv.user_id.id
            })
            return {
                'name':"Invoice Order",
                'view_mode': 'form',
                #'view_id': view_id,
                'view_type': 'form',
                'res_model': 'sale.advance.payment.inv',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': ctx,
            }



    #Redifinition pour retirer la modification auto du vendeur
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if not partner_id:
            self.value = {
                'partner_invoice_id': False, 
                'partner_shipping_id': False,  
                'payment_term': False, 
                'fiscal_position': False
            }
        else:
            part = self.env['res.partner'].browse(partner_id)
            addr = self.env['res.partner'].address_get([part.id], ['delivery', 'invoice', 'contact'])
            pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
            invoice_part = self.env['res.partner'].browse(addr['invoice'])
            payment_term = invoice_part.property_payment_term and invoice_part.property_payment_term.id or False
            dedicated_salesman = part.user_id and part.user_id.id or uid
            val = {
                'partner_invoice_id': addr['invoice'],
                'partner_shipping_id': addr['delivery'],
                'payment_term': payment_term,
                ##############################
                #'user_id': dedicated_salesman,
            }
            delivery_onchange = self.onchange_delivery_id(False, part.id, addr['delivery'], False)
            val.update(delivery_onchange['value'])
            if pricelist:
                val['pricelist_id'] = pricelist
            if not self._get_default_section_id() and part.section_id:
                val['section_id'] = part.section_id.id
            sale_note = self.get_salenote()
            if sale_note: 
                val.update({'note': sale_note})  
            
            self.value = val


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.model
    def _get_user_id(self):
        if context = self._context or {}
        return self._context.get('user_id', False)
    
    user_id = fields.Many2one(
        'res.users',
        string='Vendeur',
        readonly=True,
        default=_get_user_id,
    )




    def create_invoices(self):
        """ create invoices for the active sales orders """
        sale_obj = self.env['sale.order']
        act_window = self.env['ir.actions.act_window']
        wizard = self.browse(ids[0])
        sale_ids = self._context.get('active_ids', [])
        if wizard.advance_payment_method == 'all':
            # create the final invoices of the active sales orders
            res = sale_obj.manual_invoice(sale_ids)
            if self._context.get('open_invoices', False):
                return res
            return {'type': 'ir.actions.act_window_close'}

        if wizard.advance_payment_method == 'lines':
            # open the list view of sales order lines to invoice
            res = act_window.for_xml_id('sale', 'action_order_line_tree2')
            res['context'] = {
                'search_default_uninvoiced': 1,
                'search_default_order_id': sale_ids and sale_ids[0] or False,
            }
            return res
        assert wizard.advance_payment_method in ('fixed', 'percentage')
        
        inv_ids = []
        for sale_id, inv_values in self._prepare_advance_invoice_vals():
            inv_ids.append(self._create_invoices(inv_values, sale_id))
        
        #Ajouter par ando inv.user_id.id
        ctx = dict(self._context)
        ctx.update({
                    'default_user_id':self.browse(self._ids)[0].user_id.id
                    })
        if self._context.get('open_invoices', False):
            return self.open_invoices(inv_ids)
        return {'type': 'ir.actions.act_window_close'}