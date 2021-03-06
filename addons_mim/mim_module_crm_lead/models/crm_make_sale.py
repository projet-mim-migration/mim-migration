# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions
from openerp.tools.translate import _


class crm_make_sale(models.TransientModel):
    """ Make sale  order for crm """

    _inherit = "crm.make.sale"

    def makeOrder(self):
        
        print ("makeOrder")
        """
        This function  create Quotation on given case.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of crm make sales' ids
        @param context: A standard dictionary for contextual values
        @return: Dictionary value of created sales order.
        """
        # update context: if come from phonecall, default state values can make the quote crash lp:1017353
        context = dict(self.env.context or {})
        context.pop('default_state', False)        
        
        case_obj = self.env['crm.lead']
        sale_obj = self.env['sale.order']
        partner_obj = self.env['res.partner']
        data = context and context.get('active_ids', []) or []

        for make in self.browse():
            partner = make.partner_id
            #deux paramètre au lieu de max = 1
            partner_addr = partner_obj.address_get([partner.id],
                    ['default', 'invoice', 'delivery', 'contact'])
            pricelist = partner.property_product_pricelist.id
            fpos = partner.property_account_position and partner.property_account_position.id or False
            payment_term = partner.property_payment_term and partner.property_payment_term.id or False
            new_ids = []
            for case in case_obj.browse(data):
                if not partner and case.partner_id:
                    partner = case.partner_id
                    fpos = partner.property_account_position and partner.property_account_position.id or False
                    payment_term = partner.property_payment_term and partner.property_payment_term.id or False
                    partner_addr = partner_obj.address_get([partner.id],
                            ['default', 'invoice', 'delivery', 'contact'])
                    pricelist = partner.property_product_pricelist.id
                if False in partner_addr.values():
                    raise exceptions.Warning(_('Insufficient Data!'), _('No address(es) defined for this customer.'))

                vals = {
                    'origin': _('Opportunity: %s') % str(case.id),
                    'crm_lead_id': case.id or False,
                    'section_id': case.section_id and case.section_id.id or False,
                    'categ_ids': [(6, 0, [categ_id.id for categ_id in case.categ_ids])],
                    'partner_id': partner.id,
                    'pricelist_id': pricelist,
                    'partner_invoice_id': partner_addr['invoice'],
                    'partner_shipping_id': partner_addr['delivery'],
                    'date_order': fields.datetime.now(),
                    'fiscal_position': fpos,
                    'payment_term':payment_term,
                    'note': sale_obj.get_salenote([case.id], partner.id),
                }
                '''
                    get_salenote n'existe pas
                '''
                '''
                        get_salenote n'existe plus dans odoo 12
                        dans odoo 8 :                                    
                    def get_salenote(self, cr, uid, ids, partner_id, context=None):
                        if context is None:
                            context = {}
                        context_lang = context.copy()
                        if partner_id:
                            partner_lang = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context).lang
                            context_lang.update({'lang': partner_lang})
                        return self.pool.get('res.users').browse(cr, uid, uid, context=context_lang).company_id.sale_note


                '''
                if partner.id:
                    vals['user_id'] = partner.user_id and partner.user_id.id or self.env.uid
                new_id = sale_obj.create(vals)
                sale_order = sale_obj.browse(new_id)
                case_obj.write([case.id], {'ref': 'sale.order,%s' % new_id})
                new_ids.append(new_id)
                message = _("Opportunity has been <b>converted</b> to the quotation <em>%s</em>.") % (sale_order.name)
                case.message_post(body=message)
            if make.close:
                case_obj.case_mark_won(data)
            if not new_ids:
                return {'type': 'ir.actions.act_window_close'}
            if len(new_ids)<=1:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name' : _('Quotation'),
                    'res_id': new_ids and new_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name' : _('Quotation'),
                    'res_id': new_ids
                }
            return value


