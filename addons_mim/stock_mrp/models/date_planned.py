# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class stock_mrp (models.Model):
    _name = "mrp.configuration"


    def _get_picking_id(self):
        if self.env.context is None: self.env.context = {}
        return self.env.context.get('picking_id', False)



    def _get_date_planned(self):
        if self.env.context is None: self.env.context = {}
        return self.env.context.get('date_planned', False)
    
    
    date_planned = fields.Date('Date plannifiée', required=True, compute=_get_picking_id)
    picking_id = fields.Integer('Id current picking line', compute=_get_date_planned)
    
    def update_move_data(self):
        # TODO
        picking_id = self.picking_id #?????????????
        picking_obj = self.env["stock.picking"]
        # recuperer
        new_date_planned = self.date_planned
        for pick in picking_obj.browse([picking_id]):
            for move in pick.move_lines:
                stock_move_id = move.id
                #Creation de l'ordre de fabrication
                move_data = self.env['stock.move'].browse(stock_move_id)
                
                #move_data = self.browse(cr, uid, ids, context=context)[0]
                self.env.cr.execute('''select mrp_bom.id 
                              from mrp_bom
                              inner join product_product
                              on mrp_bom.product_id = product_product.id
                              where product_product.id={0}'''.format(move_data.product_id.id))
         
                res_req = self.env.cr.dictfetchone()
                if res_req :
                    bom_id = res_req["id"]
                else:
                    bom_id = False
                   
                #recuperation du lien avec la ligne de la commande    
                if move_data.procurement_id and move_data.procurement_id.sale_line_id:
                    sale_line_id = move_data.procurement_id.sale_line_id
                else:
                    raise UserError(_("Ce movement de stock n'\est li� � aucune ligne de bons de commande (sale.order.line)"))
                vals = {
                    'origin': move_data.origin,
                    'product_id': move_data.product_id.id,
                    'product_qty': move_data.product_qty,
                    'product_uom': move_data.product_uom.id,
                    'product_uos_qty': move_data.product_uos and move_data.product_uos_qty or False,
                    'product_uos': move_data.product_uos and move_data.product_uos.id or False,
                    'location_src_id': move_data.location_id.id,
                    'location_dest_id': move_data.location_dest_id.id,
                    'bom_id': bom_id,
                    'date_planned': new_date_planned,
                    'move_prod_id': move_data.id,
                    'company_id': move_data.company_id.id,
                    'largeur': move_data.largeur,
                    'hauteur': move_data.hauteur,
                    'is_printable':move_data.is_printable,
                    'description':move_data.name,
                    'partner_id':move_data.picking_id.partner_id.id,
                    
                    #mim wizard
                    'dimension':sale_line_id.dimension,
                    'vitre':sale_line_id.vitre.id,
                    'type_vitre':sale_line_id.type_vitre,
                    'decoratif' :sale_line_id.decoratif.id, 
                    'poigne' :sale_line_id.poigne.id,
                    'nb_poigne':sale_line_id.nb_poigne,
                    'serr' :sale_line_id.serr.id,
                    'nb_serr':sale_line_id.nb_serr,
                    'oscillo_battant':sale_line_id.oscillo_battant,
                    'va_et_vient':sale_line_id.va_et_vient,
                    'butoir':sale_line_id.butoir,
                    'remplissage_vitre':sale_line_id.remplissage_vitre,
                    'type_fixe':sale_line_id.type_fixe,
                    'inegalite':sale_line_id.inegalite,
                    'cintre':sale_line_id.cintre,
                    'triangle':sale_line_id.triangle,
                    'division':sale_line_id.division,
                    'nb_division':sale_line_id.nb_division,
                    'laque':sale_line_id.laque,
                    'moustiquaire':sale_line_id.moustiquaire,
                    'tms':sale_line_id.tms,
                    'type_moustiquaire':sale_line_id.type_moustiquaire,
                    'intermediaire':sale_line_id.intermediaire,
                    
                }
                production_obj = self.env['mrp.production']
                stock_move_obj = self.env['stock.move']
                id_mo = production_obj.create(vals)
                val = {}
                val['id_mo'] = id_mo
                val['user_id'] = self.env.uid
                val['is_mo_created'] = True
                
                stock_move_obj.write( [stock_move_id], val)
            #picking_obj.write(cr, uid, [pick.id], {'mo_created':True}, context=context)        
        return True