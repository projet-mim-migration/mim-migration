# -*- coding: utf-8 -*-

from odoo import fields, models, api

    
class CrmClaim(models.Model):
    _inherit = "crm.claim"
    
    stage_id = fields.Many2one(
        'crm.claim.stage', 
        'Stage', 
        domain="['|', ('team_ids', '=', team_id), ('case_default', '=', True)]",
        default=1,
        track_visibility='onchange'
    )
                
    @api.multi
    def action_set_to_draft(self):
        self.write({'stage_id': 1})
        return True
    
    @api.multi
    def action_confirm(self):
        id = self.env['ir.model.data'].get_object_reference('crm_claim_inherit', 'stage_claim4')
        stage_id = id[1]
        self.write({'stage_id': stage_id})
        return True
        
    @api.multi
    def action_open(self):
        self.write({'stage_id': 2})
        return True
        
    @api.multi
    def action_done(self):
        self.write({'stage_id': 3})
        return True
    
    @api.multi
    def action_cancel(self):
        self.write({'stage_id': 4})
        return True