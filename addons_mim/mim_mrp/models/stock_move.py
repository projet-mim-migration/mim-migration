# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def _get_test_group(self):
        for sm in self:
            flag = self.env['res.users'].has_group('mim_mrp.mrp_valider')
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
    def action_view_mo(self):
        self.ensure_one()

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