# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    crm_lead_id = fields.Many2one(
        'crm.lead', 
        u'Opportunité', 
        select=True, 
        track_visibility='onchange',
    )

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _order = 'date_action'

    def _devis_count(self):
        Event = self.env['sale.order']
        self.devis_count = Event.search_count([('crm_lead_id', '=', self.ids[0])])
        

    # event when date action changed
    @api.onchange('date_action')
    def _onchange_date_action(self):
        self.date_changed = True
        self.motivation = False


    devis_ids = fields.One2many(
        'sale.order', 
        'crm_lead_id', 
        'Devis', 
        readonly=True, 
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, 
        copy=True
    )
    devis_count = fields.Integer(
        string='# Meetings',
        compute='_devis_count',
    )

    title_action = fields.Char()
    date_action = fields.Date(string=u'Prochaine action')
    motivation = fields.Text('Motif')
    date_changed = fields.Boolean('Date changed',default=False)
    date_action_old = fields.Date(u'Date prochaine action (précédente)')
    date_modification = fields.Date(u'Date dernière modification')
    title_action_old = fields.Char(u'Prochaine action (précédente)')
   


    def action_devis(self):
        """
        Open meeting's calendar view to schedule meeting on current opportunity.
        :return dict: dictionary value for created Meeting view
        """
        lead = self
        res = self.env['ir.actions.act_window'].for_xml_id('sale', 'action_quotations')
        partner_ids = [self.env['res.users'].partner_id.search([])]
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
    
    
    def write(self, values):
        if values.get('date_changed') and values['date_changed'] == True:
            if values.get('motivation') and values['motivation'] not in ('', False):
                description = self.description
                if not description:
                    description = ''
                date_action = values['date_action']
                if values.get('title_action'):
                    title_action = values['title_action']
                else: 
                    if self.title_action:
                        title_action = self.title_action
                    else:
                        title_action = ''
                current_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
                
                new_description = '[Date modification: ' + current_date + ', ' + 'Motif modification: ' + values['motivation'] + ', ' + ' Date prochaine action: ' + date_action + ', ' + ' Prochaine action: ' + title_action + ']'
                desc = values['motivation']
                values['description'] = new_description +'\n'+ description
                values['date_changed'] = False
                values['motivation'] = False
                values['date_action_old'] = self.date_action
                values['title_action_old'] = self.title_action
                values['date_modification'] = current_date
            else:
                raise exceptions.UserError('Merci de saisir la motivation de votre modification')
        
        return super(CrmLead, self).write(values)
