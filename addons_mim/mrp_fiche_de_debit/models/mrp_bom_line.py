# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpBomLine(models.Model):  
    _inherit = 'mrp.bom.line'

    ref = fields.Char(
        'Référence'
    )
    is_accessory = fields.Boolean(
        'Est un accesoire',
        default=False
    )
    component_exist = fields.Boolean(
        'Composant existe',
        default=False
    )
    component_id = fields.Integer(
        'Composant'
    )
                
    _sql_constraints = [
        ('reference_unique', 'unique(ref)', 'Il y a des doublons dans la colonne référence!')
    ]
    

    @api.multi
    def open_view_component(self):
        self.ensure_one()
        context = dict(self.env.context or {})

        product_id = self.product_id
        view_ref = self.env['ir.model.data'].get_object_reference('mrp_fiche_de_debit', 'mrp_configuration_component_form_view2')
        view_id = view_ref and view_ref[1] or False,
        component_exist = self.component_exist

        if not component_exist:
            return {
                'type' : 'ir.actions.act_window',
                'name' : 'Ajouter les sous-composants',
                'res_model' : 'mrp.component',
                'view_type' : 'form',
                'view_mode' : 'form',
                'view_id' : view_id,
                'target' : 'new',
                'nodestroy' : True,
                'context' : {
                    'default_product_parent_id' : product_id.id,
                    'default_line_id' : self.id, 
                    'default_component_exist' : component_exist,          
                },
            }
        else:
            return {
                'type' : 'ir.actions.act_window',
                'name' : 'Modifier les sous-composants',
                'res_model' : 'mrp.component',
                'res_id' : self.component_id,
                'view_type' : 'form',
                'view_mode' : 'form',
                'view_id' : view_id,
                'target' : 'new',
                'nodestroy' : True,
            }