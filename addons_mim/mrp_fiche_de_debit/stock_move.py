# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from openerp import netsvc

class stock_move (osv.osv):
    def _get_test_group(self, cr, uid, ids, name, arg, context=None):
        result = dict.fromkeys(ids, False)
        for sm in self.browse(cr, uid, ids, context=context):
            flag = self.pool.get('res.users').has_group(cr, uid, 'base.mrp_valider')
            result[sm.id] = flag
        return result
    
    _inherit = 'stock.move'
    _columns = {
                'largeur': fields.float('Largeur'),
                'hauteur': fields.float('Hauteur'),
                'id_mo':fields.integer('ID manufacturing order'),
                'user_id': fields.many2one('res.users', 'Créateur ordre de fabrication'),
                'is_printable':fields.boolean('Fiche de débit standard'),
                'is_mo_created':fields.boolean('Ordre de fabrication créé'),
                
                'in_mrp_valider_group':fields.function(_get_test_group, type='boolean',
            string='Utilisateur courant dans le groupe "Valider la fiche de débit"')
                
                }
    _defaults = {
                 'is_printable':False,
                 'is_mo_created':False,
                 }
    def edit_contre_mesure(self, cr, uid, ids, context=None):
        ctx = dict()
        ctx.update({
            'default_stock_move_id': self.browse(cr, uid, ids, context=context)[0].id
        })
        return {
            'name': 'Saisie Contre mesure',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contremesure',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }
        
    def create_mo(self, cr, uid, ids, context=None):
        move_data = self.browse(cr, uid, ids, context=context)[0]
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
                    'dimension':move_data.sale_line_id.dimension,
                    'vitre':move_data.sale_line_id.vitre.id,
                    'type_vitre':move_data.sale_line_id.type_vitre,
                    'decoratif' :move_data.sale_line_id.decoratif.id, 
                    'poigne' :move_data.sale_line_id.poigne.id,
                    'nb_poigne':move_data.sale_line_id.nb_poigne,
                    'serr' :move_data.sale_line_id.serr.id,
                    'nb_serr':move_data.sale_line_id.nb_serr,
                    'oscillo_battant':move_data.sale_line_id.oscillo_battant,
                    'va_et_vient':move_data.sale_line_id.va_et_vient,
                    'butoir':move_data.sale_line_id.butoir,
                    'remplissage_vitre':move_data.sale_line_id.remplissage_vitre,
                    'type_fixe':move_data.sale_line_id.type_fixe,
                    'inegalite':move_data.sale_line_id.inegalite,
                    'cintre':move_data.sale_line_id.cintre,
                    'triangle':move_data.sale_line_id.triangle,
                    'division':move_data.sale_line_id.division,
                    'nb_division':move_data.sale_line_id.nb_division,
                    'laque':move_data.sale_line_id.laque,
                    'moustiquaire':move_data.sale_line_id.moustiquaire,
                    'tms':move_data.sale_line_id.tms,
                    'type_moustiquaire':move_data.sale_line_id.type_moustiquaire,
                    'intermediaire':move_data.sale_line_id.intermediaire,
                    
                }
                production_obj = self.pool.get('mrp.production')
                stock_move_obj = self.pool.get('stock.move')
                id_mo = production_obj.create(cr, uid, vals, context=context)
                val = {}
                val['id_mo'] = id_mo
                val['user_id'] = uid
                val['is_mo_created'] = True
                
                stock_move_obj.write(cr, uid, ids, val, context=context)
            else: 
                raise osv.except_osv(('Erreur'), (u'Il n\'existe pas de nomenclature pour cet article.\n Veuillez en crÃ©er une dans Manufacturing'))
        else: 
                raise osv.except_osv(('Erreur'), (u'Veuillez saisir les contre-mesures avant de valider.'))        
            
        return True
    def action_view_mo(self, cr, uid, ids, context=None):
        id_mo = self.browse(cr, uid, ids, context=context)[0].id_mo
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'mrp', 'mrp_production_form_view')
        view_id = view_ref and view_ref[1] or False,
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ordre de fabrication',
            'res_model': 'mrp.production',
            'res_id': id_mo,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
        
    def confirm_config_mo(self, cr, uid, ids, context=None):
        ctx = dict()
        ctx.update({
            'default_is_printable': self.browse(cr, uid, ids, context=context)[0].is_printable,
            'default_stock_move_id': self.browse(cr, uid, ids, context=context)[0].id
        })
        return {
            'name': u'Veuillez cocher la case si la fiche de débit est une fiche standard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'choice.configuration',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }
    
    """def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        return  osv.osv.write(self, cr, uid, ids, vals, context=context)"""   
stock_move()