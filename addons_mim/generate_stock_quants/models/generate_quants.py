# -*- coding: utf-8 -*-

from odoo import models, fields, api

class generate_quants(models.Model):
    
    _name="gene.models"
    
    visible = fields.Boolean("Visible",default=False)


    def get_product_id_move(self):
        
        self.env.cr.execute("select distinct(product_id) from stock_move where state='done' order by product_id")
        list_product = []
        res= self.env.cr.fetchall()
        for i in range(len(res)):
            list_product.append(res[i][0])
        return list_product
    
    def creation_inventaire(self):
        list_product = self.get_product_id_move()
        
        if self.env.context is None:
            self.env.context = {}

        inventory_obj = self.env['stock.inventory']
        inventory_line_obj = self.env['stock.inventory.line']
        inventory_id = inventory_obj.create({
                'name': 'INV Migrations Produits',
                'filter': 'partial',
                'location_id': 12,#12 signifie le stock_dans Physical Locations / WH / Stock dans la table stock_location
                 })
        for i in list_product:
            self.env.cr.execute("select ((select coalesce(sum(product_qty),0) from stock_move where state='done' \
                        and location_dest_id=12 and product_id={}) - (select coalesce(sum(product_qty),0) \
                        from stock_move where state='done' and location_id=12 and product_id={})) as sum".format(i,i)) ;
            res = self.env.cr.fetchall()
            self.env.cr.execute("select product_template.uom_id from product_product \
                        inner join product_template on product_product.product_tmpl_id=product_template.id\
                        where product_product.id={}".format(i))
            res1 = self.env.cr.fetchall()
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
                inventory_line_obj.create(line_data)
     
                
        inventory_id._action_done()    
                   
        gener_obj = self.env['gene.models']
        print(self.ids[0])
        gener_obj.search([('id','=',self.ids[0])]).write({'visible':True})
        
    def update_inventory(self):
        if self.env.context is None:
            self.env.context = {}
            
        inventory_obj = self.env['stock.inventory']
        inventory_line_obj = self.env['stock.inventory.line']
        prod_inv_obj = self.env['product.packaging']
        prod_obj = self.env['product.product']
        
        inventory_id = inventory_obj.create({
                'name': 'INV Update Product Quantity available',
                'filter': 'partial',
                'location_id': 12,
                 })
        prod_ids = prod_obj.search([])#(self.env.cr, self.env.uid, [])
        for prod_id in prod_ids:
            self.env.cr.execute("SELECT p2.uom_id FROM product_product p1 \
                        INNER JOIN product_template p2 ON p1.product_tmpl_id=p2.id\
                        WHERE p1.id={}".format(prod_id.id))#prod_id
            res = self.env.cr.fetchall()
            uom_id=res[0][0]
            prod_inv_ids = prod_inv_obj.search([('product_id','=',prod_id.id)])#prod_id
            qty_available = prod_inv_obj.browse(prod_inv_ids).qty
            
            if(qty_available>0):
                line_data = {
                    'inventory_id': inventory_id,
                    'product_qty': qty_available,
                    'location_id':12,
                    'product_id': prod_id.id,
                    'product_uom_id': uom_id
                    }           
                inventory_line_obj.create(line_data)
     
                
        inventory_id._action_done()
            