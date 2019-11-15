# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions,api
from odoo import netsvc

class HrHolidays(models.Model):
    _inherit = 'hr.leave'
    
    @api.multi
    def write(self, values):
        employee_id = values.get('employee_id', False)
        hr_holiday_id = super(HrHolidays, self).write(values)#models.Model.write(self, values)
        self.add_follower(employee_id)
        return hr_holiday_id

    '''@api.model
                def write(self, vals):
                    print('**********************************************')
                    print('**********************************************')
                    print('**********************************************')
                    employee_id = vals.get('employee_id', False)
                    #enlever pour que le nouveau senario marche
                    #if vals.get('state') and vals['state'] not in ['draft', 'confirm', 'cancel'] and not self.pool['res.users'].has_group(cr, uid, 'base.group_hr_user'):
                        # raise osv.except_osv(_('Warning!'), _('You cannot set a leave request as \'%s\'. Contact a human resource manager.') % vals.get('state'))
                    #hr_holiday_id = super(hr_holidays, self).write(cr, uid, ids, vals, context=context)
                    hr_holiday_id = models.Model.write(self, vals)
                    self.add_follower(employee_id)
                    return hr_holiday_id'''

    @api.multi    
    def test_manager(self):
        for holiday in self:
            if not holiday.employee_id.parent_id:
                manager_id = holiday.employee_id.department_id.manager_id
            else: 
                manager_id = holiday.employee_id.coach_id
            user_id = manager_id.user_id.id
            if self.env.user.id in (user_id,):
<<<<<<< HEAD
                self.env['hr.leave'].search([('id','=',self.ids[0])]).write({'state':'validate'})
                #netsvc.LocalService("workflow").trg_validate('hr.leave', holiday.id, 'validate')
=======
                self.browse(holiday.id).state = 'validate'
>>>>>>> 9df51df2281ea06c13dc3d8f43f5abfbc73077ec
            else:
                raise exceptions.UserError((u"Seul le Résponsable hiérarchique %s a le droit d'approuver la demande de congé de  %s" \
                                         % (manager_id.name,holiday.employee_id.name)))
        return True

            
            
        
        
        