# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api


class ChoiceConfiguration (models.Model):
    _name = 'choice.configuration'

    def _get_stock_move_id(self):
        context = self.env.context or {}
        return context.get('stock_move_id', False)

    def _get_is_printable(self):
        context = self.env.context or {}
        return context.get('is_printable', False)
    
    is_printable = fields.Boolean(
        string='La fiche de débit est une fiche standard',
        help='Veuillez cocher si la fiche de débit est une fiche standard', 
        default=_get_is_printable,
    )
    stock_move_id = fields.Integer(
        string='Id current stock move line',
        default=_get_stock_move_id,
    )


    @api.multi
    def update_move_data(self):
        self.ensure_one()

        move_data = self.env['stock.move'].browse(self.stock_move_id)
        move_data.write({
            'is_printable' : self.is_printable
        })
    
        # Création de l'ordre de fabrication
        self.env.cr.execute('''SELECT mrp_bom.id 
                      FROM mrp_bom
                      INNER JOIN product_product
                      ON mrp_bom.product_id = product_product.id
                      WHERE product_product.id={0}'''.format(move_data.product_id.id))
 
        res_req = self.env.cr.dictfetchone()
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
                raise exceptions.UserError("Ce movement de stock n'est lié à aucune ligne de bons de commande (sale.order.line)")
            vals = {
                'origin' : move_data.origin,
                'product_id' : move_data.product_id.id,
                'product_qty' : move_data.product_qty,
                'product_uom' : move_data.product_uom.id,
                # 'product_uos_qty' : move_data.product_uos and move_data.product_uos_qty or False,
                # 'product_uos' : move_data.product_uos and move_data.product_uos.id or False,
                'location_src_id' : move_data.location_id.id,
                'location_dest_id' : move_data.location_dest_id.id,
                'bom_id' : bom_id,
                'date_planned' : move_data.date_expected,
                # 'move_prod_id' : move_data.id,
                'company_id' : move_data.company_id.id,
                'largeur' : move_data.largeur,
                'hauteur' : move_data.hauteur,
                'is_printable' : move_data.is_printable,
                'description' : move_data.name,
                'partner_id' : move_data.picking_id.partner_id.id,
                
                #mim wizard
                'dimension' : sale_line_id.dimension,
                'vitre' : sale_line_id.vitre.id,
                'type_vitre' : sale_line_id.type_vitre,
                'decoratif' : sale_line_id.decoratif.id, 
                'poigne' : sale_line_id.poigne.id,
                'nb_poigne' : sale_line_id.nb_poigne,
                'serr' : sale_line_id.serr.id,
                'nb_serr' : sale_line_id.nb_serr,
                'oscillo_battant' : sale_line_id.oscillo_battant,
                'va_et_vient' : sale_line_id.va_et_vient,
                'butoir' : sale_line_id.butoir,
                'remplissage_vitre' : sale_line_id.remplissage_vitre,
                'type_fixe' : sale_line_id.type_fixe,
                'inegalite' : sale_line_id.inegalite,
                'cintre' : sale_line_id.cintre,
                'triangle' : sale_line_id.triangle,
                'division' : sale_line_id.division,
                'nb_division' : sale_line_id.nb_division,
                'laque' : sale_line_id.laque,
                'moustiquaire' : sale_line_id.moustiquaire,
                'tms' : sale_line_id.tms,
                'type_moustiquaire' : sale_line_id.type_moustiquaire,
                'intermediaire' : sale_line_id.intermediaire,
            }

            id_mo = self.env['mrp.production'].create(vals)
            val = {
                'id_mo' : id_mo,
                'user_id' : self.env.user.id,
                'is_mo_created' : True,
            }
            
            self.env['stock.move'].browse(self.stock_move_id).write(val)
        else:
            raise exceptions.UserError('Veuillez saisir les contre-mesures avant de valider.')
            
        return True