# -*- coding: utf-8 -*-
from odoo import models, fields, api


class mim_crm_lead (models.Model):
    _inherit = 'crm.lead'
    
    def _devis_count(self):
        Event = self.env['sale.order']
        self.devis_count = Event.search_count([('crm_lead_id', '=', self.ids[0])])
        '''return {
                                    opp_id : Event.search_count([('crm_lead_id', '=', opp_id)])
                                    for opp_id in self.ids
                                }'''
        
    devis_ids = fields.One2many('sale.order', 'crm_lead_id', 'Devis', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True)
    devis_count = fields.Integer(compute=_devis_count, string='# Meetings')
   
    def action_devis(self):
        """
        Open meeting's calendar view to schedule meeting on current opportunity.
        :return dict: dictionary value for created Meeting view
        """
        lead = self
        res = self.env['ir.actions.act_window'].for_xml_id('sale', 'action_quotations')
        partner_ids = [self.env['res.users'].browse().partner_id.id]
        if lead.partner_id:
            partner_ids.append(lead.partner_id.id)
        res['context'] = {
            'search_default_opportunity_id': lead.type == 'opportunity' and lead.id or False,
            'default_opportunity_id': lead.type == 'opportunity' and lead.id or False,
            'default_crm_lead_id': lead.type == 'opportunity' and lead.id or False,
            'default_partner_id': lead.partner_id and lead.partner_id.id or False,
            'default_partner_ids': partner_ids,
            #'default_section_id': lead.section_id and lead.section_id.id or False,
            'default_name': lead.name,
        }
        res['domain'] = "[('crm_lead_id', 'in', %s)]" % self.ids
        
        return res