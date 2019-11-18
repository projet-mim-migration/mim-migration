# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Invoice2(models.Model):
    _inherit = 'account.invoice'

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
    
    # PROBLEM Unknow relation

    # categ_ids = fields.Many2many(
    #     'crm.case.categ', 
    #     'sale_order_category_rel', 
    #     'order_id', 
    #     'category_id', 
    #     'Tags',
    #     domain="['|', ('section_id', '=', section_id), ('section_id', '=', False), ('object_id.model', '=', 'crm.lead')]", 
    #     context="{'object_name': 'crm.lead'}", 
    #     required=True
    # )


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

 
    @api.multi
    def create_invoice_new(self):
        self.ensure_one()

        ctx = dict(self._context)

        ctx.update({
            'default_user_id':self.user_id.id
        })
        return {
            'name':"Invoice Order",
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'sale.advance.payment.inv',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }

    # Redifinition pour retirer la modification auto du vendeur
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            # 'user_id': self.partner_id.user_id.id or self.partner_id.commercial_partner_id.user_id.id or self.env.uid
            ###############################
        }
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_sale_note') and self.env.user.company_id.sale_note:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note

        if self.partner_id.team_id:
            values['team_id'] = self.partner_id.team_id.id
        self.update(values)



class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.model
    def _get_user_id(self):
        context = self._context or {}
        return context.get('user_id', False)
    
    user_id = fields.Many2one(
        'res.users',
        string='Vendeur',
        readonly=True,
        default=_get_user_id,
    )


    @api.multi
    def create_invoices(self):
        #Ajouter par ando inv.user_id.id
        ctx = dict(self._context)
        ctx.update({
            'default_user_id':self.user_id.id
        })

        return super(SaleAdvancePaymentInv, self).create_invoices()