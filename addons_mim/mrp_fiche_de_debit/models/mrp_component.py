# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpComponent(models.Model):
    _name = 'mrp.component'

    def _get_product_parent_id(self):
        context = dict(self._context or {})
        return context.get('product_parent_id', False)
    def _get_line_id(self):
        context = dict(self._context or {})
        return context.get('line_id', False)
    def _get_component_exist(self):
        context = dict(self._context or {})
        return context.get('component_exist', False)

    product_parent_id = fields.Many2one(
        'product.product',
        'Article parent', 
        ondelete='cascade',
        default=_get_product_parent_id
    )
    sub_component_ids = fields.One2many(
        'mrp.sub.component',
        'component_id',
        'Sous-composants', 
    )
    line_id = fields.Many2one(
        'mrp.bom.line',
        'Bom line parent', 
        ondelete='cascade',
        default=_get_line_id
    )
    component_exist = fields.Boolean(
        'Composant existe',
        default=_get_component_exist
    )
    variable = fields.Text(
        'Variables utilisables',
        help='Ces variables sont utilisables dans les calculs en code python',
        default='''            Q : Quantité article parent, 
            largeur : Largeur de l'article, 
            hauteur : Hauteur de l'article, 
            QU : Quantité unitaire, 
            QT : Quantité total, 
            LU : Longueur unitaire, 
            style : fr ou en, 
            vitre : standard, pleine_bardage, pleine_2_3, pleine_1_2, pleine_1_3 (remplissage vitre)''',
    )
                

    
    #Cette fonction permet de sauvegarder pour la première fois le contenu 
    #du sous composant mrp_component après ce sera l fonction write sera utilisée car component_exist est à True
    @api.multi
    def save_component(self):
        self.ensure_one()
        comp_obj = self.env['mrp.component']
        bom_line_obj = self.env['mrp.bom.line']
        
        vals = {
                'product_parent_id': self.product_parent_id.id,
                'line_id':self.line_id.id,
                'component_exist':True,
                }     
        comp_obj.search(['id', '=', self.id]).write(vals)
        #component_id est nécéssaire pour réouvrir l'objet mrp_component (res_id) avec la fonction de mrp_bom_line open_view_component()
        #component_exist pour dire que le sous composant a déjà été créé
        val = {
            'component_exist' : True,
            'component_id' : self.id
        }
        bom_line_obj.search(['line_id.id', '=', self.line_id.id]).write(val)
        
        return {
            'type' : 'ir.actions.act_window_close'
        }    
