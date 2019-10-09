from openerp.osv import fields,osv

class invoice2(osv.osv):
    def _get_user_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('user_id', False)
    
    _inherit = 'account.invoice'
    _columns = {
                'user_id': fields.many2one('res.users', 'Salesperson', readonly=True, track_visibility='onchange', states={'draft':[('readonly',False)]}),
                }
    _defaults = {
                 'user_id': _get_user_id ,
                 }
class sale_order(osv.osv):
    
    _inherit = 'sale.order'
    _columns = {
                'user_id': fields.many2one('res.users', 'Salesperson', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, select=True, track_visibility='onchange', required=True),
                'categ_ids': fields.many2many('crm.case.categ', 'sale_order_category_rel', 'order_id', 'category_id', 'Tags', \
            domain="['|', ('section_id', '=', section_id), ('section_id', '=', False), ('object_id.model', '=', 'crm.lead')]", context="{'object_name': 'crm.lead'}", required=True),
                }
    
    _defaults = {
                 'user_id': False,
                 }
    def create_invoice_new(self, cr, uid, ids, context=None): 
        #view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_sale_advance_payment_inv')
        inv = self.browse(cr, uid, ids[0], context=context)
        ctx = dict(context)
        ctx.update({
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
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value': {'partner_invoice_id': False, 'partner_shipping_id': False,  'payment_term': False, 'fiscal_position': False}}

        part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        addr = self.pool.get('res.partner').address_get(cr, uid, [part.id], ['delivery', 'invoice', 'contact'])
        pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
        invoice_part = self.pool.get('res.partner').browse(cr, uid, addr['invoice'], context=context)
        payment_term = invoice_part.property_payment_term and invoice_part.property_payment_term.id or False
        dedicated_salesman = part.user_id and part.user_id.id or uid
        val = {
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'payment_term': payment_term,
            ##############################
            #'user_id': dedicated_salesman,
        }
        delivery_onchange = self.onchange_delivery_id(cr, uid, ids, False, part.id, addr['delivery'], False,  context=context)
        val.update(delivery_onchange['value'])
        if pricelist:
            val['pricelist_id'] = pricelist
        if not self._get_default_section_id(cr, uid, context=context) and part.section_id:
            val['section_id'] = part.section_id.id
        sale_note = self.get_salenote(cr, uid, ids, part.id, context=context)
        if sale_note: val.update({'note': sale_note})  
        return {'value': val}
    
class sale_advance_payment_inv(osv.osv_memory):
    def _get_user_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('user_id', False)
    _inherit = "sale.advance.payment.inv"
    _columns = {
                'user_id': fields.many2one('res.users', 'Vendeur', readonly=True)
                }
    _defaults = {
                 'user_id':_get_user_id,
                 }
    
    def create_invoices(self, cr, uid, ids, context=None):
        """ create invoices for the active sales orders """
        sale_obj = self.pool.get('sale.order')
        act_window = self.pool.get('ir.actions.act_window')
        wizard = self.browse(cr, uid, ids[0], context)
        sale_ids = context.get('active_ids', [])
        if wizard.advance_payment_method == 'all':
            # create the final invoices of the active sales orders
            res = sale_obj.manual_invoice(cr, uid, sale_ids, context)
            if context.get('open_invoices', False):
                return res
            return {'type': 'ir.actions.act_window_close'}

        if wizard.advance_payment_method == 'lines':
            # open the list view of sales order lines to invoice
            res = act_window.for_xml_id(cr, uid, 'sale', 'action_order_line_tree2', context)
            res['context'] = {
                'search_default_uninvoiced': 1,
                'search_default_order_id': sale_ids and sale_ids[0] or False,
            }
            return res
        assert wizard.advance_payment_method in ('fixed', 'percentage')
        
        inv_ids = []
        for sale_id, inv_values in self._prepare_advance_invoice_vals(cr, uid, ids, context=context):
            inv_ids.append(self._create_invoices(cr, uid, inv_values, sale_id, context=context))
        
        #Ajouter par ando inv.user_id.id
        ctx = dict(context)
        ctx.update({
                    'default_user_id':self.browse(cr, uid, ids, context=context)[0].user_id.id
                    })
        if context.get('open_invoices', False):
            return self.open_invoices( cr, uid, ids, inv_ids, context=ctx)
        return {'type': 'ir.actions.act_window_close'}