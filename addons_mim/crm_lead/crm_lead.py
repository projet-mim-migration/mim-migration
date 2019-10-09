# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import datetime

class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    _order = 'date_action'

    _columns = {
                'motivation': fields.text('Motif'),
                'date_changed':fields.boolean('Date changed'),
                'date_action_old': fields.date(u'Date prochaine action (précédente)'),
                'date_modification': fields.date(u'Date dernière modification'),
                'title_action_old': fields.char(u'Prochaine action (précédente)'),
                }

    _defaults = {
                 'date_changed':False,
                 }
    
    
    # event when date action changed
    def _onchange_date_action(self, cr, uid, ids, context=None):
        if len(ids)>0:
            return {'value':{'date_changed': True, 'motivation': False}}
        else: return {'value':{'date_changed': False}}
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('date_changed') and vals['date_changed'] == True:
            if vals.get('motivation') and vals['motivation'] not in ('', False):
                description = self.browse(cr, uid, ids[0], context=context).description
                if not description:
                    description = ''
                date_action = vals['date_action']
                if vals.get('title_action'):
                    title_action = vals['title_action']
                else: 
                    if self.browse(cr, uid, ids[0], context=context).title_action:
                        title_action = self.browse(cr, uid, ids[0], context=context).title_action
                    else:
                        title_action = ''
                current_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
                
                new_description = '[Date modification: ' + current_date + ', ' + 'Motif modification: ' + vals['motivation'] + ', ' + ' Date prochaine action: ' + date_action + ', ' + ' Prochaine action: ' + title_action + ']'
                desc = vals['motivation']
                vals['description'] = new_description +'\n'+ description
                vals['date_changed'] = False
                vals['motivation'] = False
                vals['date_action_old'] = self.browse(cr, uid, ids[0], context=context).date_action
                vals['title_action_old'] = self.browse(cr, uid, ids[0], context=context).title_action
                vals['date_modification'] = current_date
            else:
                raise osv.except_osv(('Erreur'), ('Merci de saisir la motivation de votre modification'))
        return super(crm_lead, self).write(cr, uid, ids, vals, context=context)
