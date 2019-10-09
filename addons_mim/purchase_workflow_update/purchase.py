# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import netsvc
from openerp import SUPERUSER_ID
#from openerp.tools.translate import _

class purchase_order(osv.osv):
    
    #STATE_SELECTION = [
        #('draft', 'Draft PO'),
        #('sent', 'RFQ Sent'),
        #('confirmed', 'Waiting Approval'),
        #('approved', 'Purchase Order'),
        #('payement_invoice_ok', u'Payement établi & Facture reçue'),
        #('recept_invoice', u'Récéption facture'),
        #('except_picking', 'Shipping Exception'),
        #('except_invoice', 'Invoice Exception'),
        #('done', 'Done'),
        #('cancel', 'Cancelled')
    #]
    _inherit = "purchase.order"
    _columns = {
                #'state': fields.selection(STATE_SELECTION, 'Status', readonly=True, help="The status of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' status. Then the order has to be confirmed by the user, the status switch to 'Confirmed'. Then the supplier must confirm the order to change the status to 'Approved'. When the purchase order is paid and received, the status becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the status becomes in exception.", select=True),
                'paiement_etabli':fields.char(u'Paiement établi'),
                'facture_recue':fields.char(u'Facture reçue'),
                }
    
    def wkf_payement_not_ok(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'paiement_etabli': ''})
        return True
    def wkf_payement_ok(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'paiement_etabli': 'Oui'})
        #paiement_etabli = self.browse(cr, uid, ids, context=context)[0].paiement_etabli
        #facture_recue = self.browse(cr, uid, ids, context=context)[0].facture_recue
        #if paiement_etabli=='Oui' and facture_recue=='Oui': 
            #self.write(cr, uid, ids, {'state': 'payement_invoice_ok'})
        return True
    def wkf_recept_invoice(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'facture_recue': 'Oui'})
        #paiement_etabli = self.browse(cr, uid, ids, context=context)[0].paiement_etabli
        #facture_recue = self.browse(cr, uid, ids, context=context)[0].facture_recue
        #if paiement_etabli=='Oui' and facture_recue=='Oui': 
            #self.write(cr, uid, ids, {'state': 'payement_invoice_ok'})
        return True
    
    def get_list_id_jump_wkf(self, cr, uid, ids, context=None):
        cr.execute("select product_category.id from product_category where product_category.confirmed_wkf_ok=0")
        res = cr.fetchall()
        list_id = []
        for x in range(len(res)):
            list_id.append(res[x][0])
        return list_id
    def jump_confirmed(self, cr, uid, ids, context=None):
        tres = []
        for purchase in self.browse(cr, uid, ids, context=context):
            for line in purchase.order_line:
                if line :
                    tres.append(line.product_id.categ_id.id)
        #categ_article=['Transports']
        categ_article = self.get_list_id_jump_wkf(cr,uid, ids, context=context)
        res_bool = 1
        res_test = 1  
        for t in tres:
            if t in categ_article :
                res_bool = 1
            else:res_bool = 0
            res_test *= res_bool
        state = self.browse(cr, uid, ids, context=context)[0].state
        if (res_test == 1 and state in ['draft','sent']):
            netsvc.LocalService("workflow").trg_validate(SUPERUSER_ID, 'purchase.order', ids[0], 'purchase_confirm', cr)
        return True

    def create(self, cr, uid, vals, context=None):
        #appel de la fonction de la classe mere
        res_id = super(purchase_order, self).create(cr, uid, vals, context=context)
        #Ajout code redefiniton
        myobj = self.pool.get('purchase.order')
        ids = myobj.search(cr, uid, [])
        po_id = ids[0]
        #name = vals['name']
        #cr.execute("select purchase_order.id from purchase_order where purchase_order.name = '{0}'".format(name))
        #res = cr.dictfetchone()
        #po_id = res["id"]
        self.jump_confirmed(cr, uid, [po_id], context=context)
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        #appel de la fonction de la classe mere
        super(purchase_order, self).write(cr, uid, ids, vals, context=context)
        #Ajout code redefiniton
        #list_ids = ids
        self.jump_confirmed(cr, uid, [ids[0]], context=context)
        return True

purchase_order()