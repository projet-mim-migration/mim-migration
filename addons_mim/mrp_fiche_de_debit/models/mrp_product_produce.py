# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"
    
    @api.multi
    def consume(self):
        self.ensure_one()

        production_id = self._context.get('active_id', False)
        assert production_id, "Production Id should be specified in context as a Active ID."
        self.env['mrp.production'].action_produce(production_id, self.product_qty, 'consume', self)
        return {}
    

    @api.multi
    def consume_produce(self):
        self.ensure_one()

        production_id = self._context.get('active_id', False)
        state_move = self.env['mrp.production'].browse(production_id).move_prod_id.state
        if state_move in ('flowsheeting','assigned','done'):
            assert production_id, "Production Id should be specified in context as a Active ID."
            self.env['mrp.production'].action_produce(production_id, self.product_qty, 'consume_produce', self)
        else:
            raise exceptions.UserError("Le mouvement de stock lié à cet ordre de fabrication n'est pas dans l'état Fiche de débit, Veuillez d'abord Consommer")
        return {}
