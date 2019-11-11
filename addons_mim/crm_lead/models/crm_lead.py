# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions
import datetime

class crm_lead(models.Model):
    
    _inherit = 'crm.lead'

    _order = 'date_action'

    title_action = fields.Char()
    date_action = fields.Date(string=u'Prochaine action')
    motivation = fields.Text('Motif')
    date_changed = fields.Boolean('Date changed',default=False)
    date_action_old = fields.Date(u'Date prochaine action (précédente)')
    date_modification = fields.Date(u'Date dernière modification')
    title_action_old = fields.Char(u'Prochaine action (précédente)')
    
    # event when date action changed
    @api.onchange('date_action')
    def _onchange_date_action(self):
        print('**********************************************************************')
        print('*************************{}************************'.format(self.id))
        print('**********************************************************************')
        if len(self.ids)>0:
            return {'value':{'date_changed': True, 'motivation': False}}
        else: 
            return {'value':{'date_changed': False}}
    
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
                raise exceptions.Warning(('Erreur'), ('Merci de saisir la motivation de votre modification'))
        return super(crm_lead, self).write(values)
