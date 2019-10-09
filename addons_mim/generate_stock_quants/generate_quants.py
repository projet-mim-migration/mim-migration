from openerp.osv import osv,fields
from openerp import SUPERUSER_ID
from openerp import netsvc
from pychart.tick_mark import Null

class generate_quants(osv.osv):
    _name="gene.models"
    _columns={
              "visible":fields.boolean("Visible")
              
              }
    _defaults={
               'visible':False
               }
    def get_product_id_move(self,cr,uid,ids,context=None):
        
        cr.execute("select distinct(product_id) from stock_move where state='done' order by product_id")
        list_product =[]
        res= cr.fetchall()
        for i in range(len(res)):
            list_product.append(res[i][0])
        return list_product
    
    def creation_inventaire(self,cr,uid,ids,context=None):
        list_product=self.get_product_id_move(cr, uid, ids, context)
        
        if context is None:
            context = {}

        inventory_obj = self.pool.get('stock.inventory')
        inventory_line_obj = self.pool.get('stock.inventory.line')
        inventory_id = inventory_obj.create(cr, uid, {
                'name': 'INV Migrations Produits',
                'filter': 'partial',
        
                'location_id': 12,#12 signifie le stock_dans Physical Locations / WH / Stock dans la table stock_location
                 }, context=context)
        for i in list_product:
            cr.execute("select ((select coalesce(sum(product_qty),0) from stock_move where state='done' \
                        and location_dest_id=12 and product_id={}) - (select coalesce(sum(product_qty),0) \
                        from stock_move where state='done' and location_id=12 and product_id={})) as sum".format(i,i)) ;
            res = cr.fetchall()
            cr.execute("select product_template.uom_id from product_product \
                        inner join product_template on product_product.product_tmpl_id=product_template.id\
                        where product_product.id={}".format(i))
            res1=cr.fetchall()
            qty_available =res[0][0]
            uom=res1[0][0]  
            if(qty_available>0):
                line_data = {
                    'inventory_id': inventory_id,
                    'product_qty': qty_available,
                    'location_id':12,
                    'product_id': i,
                    'product_uom_id': uom
                    }           
                inventory_line_obj.create(cr , uid, line_data, context=context)
     
                
        inventory_obj.action_done(cr, uid, [inventory_id], context=context)    
                
        gener_obj = self.pool.get('gene.models')
        gener_obj.write(cr,uid, [ids[0]] , {'visible':True}, context=context)
        
    def update_inventory(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
            
        inventory_obj = self.pool.get('stock.inventory')
        inventory_line_obj = self.pool.get('stock.inventory.line')
        prod_inv_obj = self.pool.get('product.inventory')
        prod_obj = self.pool.get('product.product')
        
        inventory_id = inventory_obj.create(cr, uid, {
                'name': 'INV Update Product Quantity available',
                'filter': 'partial',
                'location_id': 12,
                 }, context=context)
        prod_ids = prod_obj.search(cr, uid, [])
        
        for prod_id in prod_ids:
            cr.execute("SELECT p2.uom_id FROM product_product p1 \
                        INNER JOIN product_template p2 ON p1.product_tmpl_id=p2.id\
                        WHERE p1.id={}".format(prod_id))
            res=cr.fetchall()
            uom_id=res[0][0]
            prod_inv_ids = prod_inv_obj.search(cr, uid, [('product_id','=',prod_id)])
            qty_available = prod_inv_obj.browse(cr, uid, prod_inv_ids, context=context)[0].quantity
            
            if(qty_available>0):
                line_data = {
                    'inventory_id': inventory_id,
                    'product_qty': qty_available,
                    'location_id':12,
                    'product_id': prod_id,
                    'product_uom_id': uom_id
                    }           
                inventory_line_obj.create(cr , uid, line_data, context=context)
     
                
        inventory_obj.action_done(cr, uid, [inventory_id], context=context)
            