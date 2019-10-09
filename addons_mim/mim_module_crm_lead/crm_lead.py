# -*- coding: utf-8 -*-
from openerp.osv import fields
from openerp.osv import osv


class mim_crm_lead (osv.osv):
    _inherit = 'crm.lead'
    
    def _devis_count(self, cr, uid, ids, field_name, arg, context=None):
        Event = self.pool['sale.order']
        return {
            opp_id: Event.search_count(cr,uid, [('crm_lead_id', '=', opp_id)], context=context)
            for opp_id in ids
    }
        
    _columns = {
        'devis_ids': fields.one2many('sale.order', 'crm_lead_id', 'Devis', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True),
        'devis_count': fields.function(_devis_count, string='# Meetings', type='integer'),
    }
   
    def action_devis(self, cr, uid, ids, context=None):
        """
        Open meeting's calendar view to schedule meeting on current opportunity.
        :return dict: dictionary value for created Meeting view
        """
        lead = self.browse(cr, uid, ids[0], context)
        res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'sale', 'action_quotations', context)
        partner_ids = [self.pool['res.users'].browse(cr, uid, uid, context=context).partner_id.id]
        if lead.partner_id:
            partner_ids.append(lead.partner_id.id)
        res['context'] = {
            'search_default_opportunity_id': lead.type == 'opportunity' and lead.id or False,
            'default_opportunity_id': lead.type == 'opportunity' and lead.id or False,
            'default_crm_lead_id': lead.type == 'opportunity' and lead.id or False,
            'default_partner_id': lead.partner_id and lead.partner_id.id or False,
            'default_partner_ids': partner_ids,
            'default_section_id': lead.section_id and lead.section_id.id or False,
            'default_name': lead.name,
        }
        res['domain'] = "[('crm_lead_id', 'in', %s)]" % ids
        return res
    
mim_crm_lead()    