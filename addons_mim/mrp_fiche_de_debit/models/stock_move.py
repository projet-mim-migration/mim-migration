# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def _get_test_group(self):
        for sm in self:
            flag = self.env['res.users'].has_group('mrp_fiche_de_debit.mrp_valider')
            sm.in_mrp_valider_group = flag

    
    largeur = fields.Float(
        'Largeur'
    )
    hauteur = fields.Float(
        'Hauteur'
    )
    id_mo = fields.Integer(
        'ID manufacturing order'
    )
    user_id = fields.Many2one(
        'res.users', 
        'Créateur ordre de fabrication'
    )
    is_printable = fields.Boolean(
        'Fiche de débit standard',
        default=False
    )
    is_mo_created = fields.Boolean(
        'Ordre de fabrication créé',
        default=False
    )
                
    in_mrp_valider_group = fields.Boolean(
        compute=_get_test_group,
        string='Utilisateur courant dans le groupe "Valider la fiche de débit"'
    )
                

    # ------------- OTRAN TS MIASA -------------
    @api.multi
    def edit_contre_mesure(self):
        self.ensure_one()
        
        ctx = dict()
        ctx.update({
            'default_stock_move_id' : self.id
        })
        return {
            'name' : 'Saisie Contre mesure',
            'type' : 'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode' : 'form',
            'res_model' : 'contremesure',
            'nodestroy' : True,
            'target' : 'new',
            'context' : ctx,
        }
        
    @api.multi
    def create_mo(self):
        self.ensure_one()

        self.env.cr.execute('''SELECT mrp_bom.id 
                      FROM mrp_bom
                      INNER JOIN product_product
                      ON mrp_bom.product_id = product_product.id
                      WHERE product_product.id = {0}'''.format(self.product_id.id))
 
        res_req = self.env.cr.dictfetchone()
        largeur = self.largeur
        hauteur = self.hauteur

        if (largeur!=0.0 and hauteur!=0.0):        
            if res_req :
                bom_id = res_req["id"]
                vals = {
                    'origin' : self.origin,
                    'product_id' : self.product_id.id,
                    'product_qty' : self.product_qty,
                    'product_uom_id' : self.product_uom.id,
                    # 'product_uos_qty' : self.product_uos and self.product_uos_qty or False,
                    # 'product_uos' : self.product_uos and self.product_uos.id or False,
                    'location_src_id' : self.location_id.id,
                    'location_dest_id' : self.location_dest_id.id,
                    'bom_id' : bom_id,
                    # 'move_prod_id' : self.id,
                    'company_id' : self.company_id.id,
                    'largeur' : self.largeur,
                    'hauteur' : self.hauteur,
                    'is_printable' : self.is_printable,
                    'description' : self.name,
                    'partner_id' : self.picking_id.partner_id.id,
                    'date_planned' : self.date_expected, 

                    #mim wizard
                    'dimension' : self.sale_line_id.dimension,
                    'vitre' : self.sale_line_id.vitre.id,
                    'type_vitre' : self.sale_line_id.type_vitre,
                    'decoratif' : self.sale_line_id.decoratif.id, 
                    'poigne' : self.sale_line_id.poigne.id,
                    'nb_poigne' : self.sale_line_id.nb_poigne,
                    'serr' : self.sale_line_id.serr.id,
                    'nb_serr' : self.sale_line_id.nb_serr,
                    'oscillo_battant' : self.sale_line_id.oscillo_battant,
                    'va_et_vient' : self.sale_line_id.va_et_vient,
                    'butoir' : self.sale_line_id.butoir,
                    'remplissage_vitre' : self.sale_line_id.remplissage_vitre,
                    'type_fixe' : self.sale_line_id.type_fixe,
                    'inegalite' : self.sale_line_id.inegalite,
                    'cintre' : self.sale_line_id.cintre,
                    'triangle' : self.sale_line_id.triangle,
                    'division' : self.sale_line_id.division,
                    'nb_division' : self.sale_line_id.nb_division,
                    'laque' : self.sale_line_id.laque,
                    'moustiquaire' : self.sale_line_id.moustiquaire,
                    'tms' : self.sale_line_id.tms,
                    'type_moustiquaire' : self.sale_line_id.type_moustiquaire,
                    'intermediaire' : self.sale_line_id.intermediaire,
                    
                }
                
                id_mo = self.env['mrp.production'].create(vals)
                
                val = {
                    'id_mo' : id_mo,
                    'user_id' : self.env.user.id,
                    'is_mo_created' : True,
                }
                
                self.write(val)
            else: 
                raise exceptions.UserError("Il n'existe pas de nomenclature pour cet article.\n Veuillez en créer une dans Manufacturing")
        else: 
            raise exceptions.UserError('Veuillez saisir les contre-mesures avant de valider.')
            
        return True
    
    @api.multi
    def action_view_mo(self):
        self.ensure_one()

        id_mo = self.browse()[0].id_mo
        view_ref = self.env['ir.model.data'].get_object_reference('mrp', 'mrp_production_form_view')
        view_id = view_ref and view_ref[1] or False,
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ordre de fabrication',
            'res_model': 'mrp.production',
            'res_id': self.id_mo,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
        
    @api.multi
    def confirm_config_mo(self):
        self.ensure_one()

        ctx = dict()
        ctx.update({
            'default_is_printable': self.is_printable,
            'default_stock_move_id': self.id
        })
        return {
            'name': 'Veuillez cocher la case si la fiche de débit est une fiche standard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'choice.configuration',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }