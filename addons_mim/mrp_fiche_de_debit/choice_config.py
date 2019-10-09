# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields

class choice_configuration (osv.osv):
    def _get_stock_move_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('stock_move_id', False)
    def _get_is_printable(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('is_printable', False)
    _name = 'choice.configuration'
    _columns = {
                'is_printable': fields.boolean(u'La fiche de débit est une fiche standard',help=u'Veuillez cocher si la fiche de débit est une fiche standard'),
                'stock_move_id':fields.integer('Id current stock move line'),
                }
    _defaults = {
              'is_printable':_get_is_printable,
              'stock_move_id':_get_stock_move_id,
              }
    
    def update_move_data(self, cr, uid, ids, context=None):
        stock_move_id = self.browse(cr, uid, ids, context=context)[0].stock_move_id
        self.pool.get('stock.move').write(cr, uid, [stock_move_id], {'is_printable':self.browse(cr, uid, ids, context=context)[0].is_printable})
        
        #Création de l'ordre de fabrication
        move_data = self.pool.get('stock.move').browse(cr, uid, stock_move_id, context=context)
        
        #move_data = self.browse(cr, uid, ids, context=context)[0]
        cr.execute('''select mrp_bom.id 
                      from mrp_bom
                      inner join product_product
                      on mrp_bom.product_id = product_product.id
                      where product_product.id={0}'''.format(move_data.product_id.id))
 
        res_req = cr.dictfetchone()
        largeur = move_data.largeur
        hauteur = move_data.hauteur 
        if (largeur!=0.0 and hauteur!=0.0):        
            if res_req :
                bom_id = res_req["id"]
            else:
                bom_id = False
               
            #Récupération du lien avec la ligne de la commande    
            if move_data.procurement_id and move_data.procurement_id.sale_line_id:
                sale_line_id = move_data.procurement_id.sale_line_id
            else:
                raise osv.except_osv(('Erreur'), (u"Ce movement de stock n'\est lié à aucune ligne de bons de commande (sale.order.line)"))    
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
                'date_planned': move_data.date_expected,
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
            production_obj = self.pool.get('mrp.production')
            stock_move_obj = self.pool.get('stock.move')
            id_mo = production_obj.create(cr, uid, vals, context=context)
            val = {}
            val['id_mo'] = id_mo
            val['user_id'] = uid
            val['is_mo_created'] = True
            
            stock_move_obj.write(cr, uid, [stock_move_id], val, context=context)
        else:
            raise osv.except_osv(('Erreur'), (u'Veuillez saisir les contre-mesures avant de valider.'))
            
        return True
        
choice_configuration()