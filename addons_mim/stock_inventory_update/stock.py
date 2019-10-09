# -*- coding: utf-8 -*-

from openerp.osv import osv

class stock_inventory_line(osv.osv):
    _inherit = "stock.inventory.line"
    
    def onchange_createline(self, cr, uid, ids, location_id=False, product_id=False, uom_id=False, package_id=False, prod_lot_id=False, partner_id=False, company_id=False, context=None):
        quant_obj = self.pool["stock.quant"]
        uom_obj = self.pool["product.uom"]
        res = {'value': {}}
        # If no UoM already put the default UoM of the product
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            uom = self.pool['product.uom'].browse(cr, uid, uom_id, context=context)
            
            #Initialiser l'uom de la ligne de l'inventaire avec l'uom de l'article choisi
            res['value']['product_uom_id'] = product.uom_id.id
            res['domain'] = {'product_uom_id': [('category_id','=',product.uom_id.category_id.id)]}
            uom_id = product.uom_id.id
            #===================================================================
            # if product.uom_id.category_id.id != uom.category_id.id:
            #     res['value']['product_uom_id'] = product.uom_id.id
            #     res['domain'] = {'product_uom_id': [('category_id','=',product.uom_id.category_id.id)]}
            #     uom_id = product.uom_id.id
            #===================================================================
            
        # Calculate theoretical quantity by searching the quants as in quants_get
        if product_id and location_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            if not company_id:
                company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
            dom = [('company_id', '=', company_id), ('location_id', '=', location_id), ('lot_id', '=', prod_lot_id),
                        ('product_id','=', product_id), ('owner_id', '=', partner_id), ('package_id', '=', package_id)]
            quants = quant_obj.search(cr, uid, dom, context=context)
            th_qty = sum([x.qty for x in quant_obj.browse(cr, uid, quants, context=context)])
            if product_id and uom_id and product.uom_id.id != uom_id:
                th_qty = uom_obj._compute_qty(cr, uid, product.uom_id.id, th_qty, uom_id)
            res['value']['theoretical_qty'] = th_qty
            res['value']['product_qty'] = th_qty
        return res
