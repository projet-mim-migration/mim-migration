# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import netsvc

class hr_holidays(osv.osv):
    _inherit = 'hr.holidays'
    def write(self, cr, uid, ids, vals, context=None):
        employee_id = vals.get('employee_id', False)
        #enlever pour que le nouveau senario marche
        #if vals.get('state') and vals['state'] not in ['draft', 'confirm', 'cancel'] and not self.pool['res.users'].has_group(cr, uid, 'base.group_hr_user'):
            # raise osv.except_osv(_('Warning!'), _('You cannot set a leave request as \'%s\'. Contact a human resource manager.') % vals.get('state'))
        #hr_holiday_id = super(hr_holidays, self).write(cr, uid, ids, vals, context=context)
        hr_holiday_id = osv.osv.write(self, cr, uid, ids, vals, context=context)
        self.add_follower(cr, uid, ids, employee_id, context=context)
        return hr_holiday_id
    def test_manager(self, cr, uid, ids, context=None):
        for holiday in self.browse(cr, uid, ids, context):
            if not holiday.employee_id.manager:
                manager_id = holiday.employee_id.department_id.manager_id
            else: 
                manager_id = holiday.employee_id.coach_id
            user_id = manager_id.user_id.id
            if uid in (user_id,):
                netsvc.LocalService("workflow").trg_validate(uid, 'hr.holidays', holiday.id, 'validate', cr)
            else: raise osv.except_osv(('Erreur')\
                                       ,(u"Seul le Résponsable hiérarchique %s a le droit d'approuver la demande de congé de  %s" \
                                         % (manager_id.name,holiday.employee_id.name)))
        return True
hr_holidays()
            
            
        
        
        