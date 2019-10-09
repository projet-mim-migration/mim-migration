# -*- coding: utf-8 -*-
from openerp.osv import fields,osv

class hr_payslip(osv.osv):
    _inherit = 'hr.payslip'
    
    _columns = {
        'etat_salaire_id': fields.many2one('etat.salaire2',string='Etat salaire'),
        'ostie_id': fields.many2one('ostie',string='Etat OSTIE'),
        'irsa_id': fields.many2one('irsa2',string='Etat IRSA'),
        'cnaps_id': fields.many2one('cnaps2',string='Etat CNAPS'),
        }
    def create(self, cr, uid, vals, context=None):
        payslip_id = super(hr_payslip, self).create(cr, uid, vals, context=context)
        data = self.pool.get('hr.payslip').browse(cr, uid, [payslip_id], context)[0]
        vals = {
                'employee_id': data.employee_id.id,
                'num_emp': data.employee_id.num_emp,
                'num_cin': data.employee_id.num_cin,
                'name_related': data.employee_id.name,
                'date_from': data.date_from,
                'date_to': data.date_to,
                }
        etat_id = self.pool.get('etat.salaire2').create(cr, uid, vals, context=context)
        ostie_id = self.pool.get('ostie').create(cr, uid, vals, context=context)
        irsa_id = self.pool.get('irsa2').create(cr, uid, vals, context=context)
        cnaps_id = self.pool.get('cnaps2').create(cr, uid, vals, context=context)
        self.pool.get('hr.payslip').write(cr, uid, [data.id], {
                                                               'etat_salaire_id': etat_id, 
                                                               'ostie_id': ostie_id, 
                                                               'irsa_id': irsa_id, 
                                                               'cnaps_id': cnaps_id
                                                               }, context=context)
        
        return payslip_id

    def write(self, cr, uid, ids, vals, context=None):
        super(hr_payslip, self).write(cr, uid, ids, vals, context=context)
        for data in self.browse(cr, uid, ids, context=context):
            if data.etat_salaire_id or data.ostie_id:
                vals = {
                    'employee_id': data.employee_id.id,
                    'num_emp': data.employee_id.num_emp,
                    'num_cin': data.employee_id.num_cin,
                    'name_related': data.employee_id.name,
                    'date_from': data.date_from,
                    'date_to': data.date_to,
                    }
                for line in data.line_ids:
                    if line.code == 'BASIC':
                        vals['basic'] = line.total 
                    if line.code == 'OMSI_EMP': 
                        vals['omsi'] = line.total
                    if line.code == 'CNAPS_EMP':
                        vals['cnaps'] = line.total
                    if line.code == 'GROSS':
                        vals['brut'] = line.total
                    if line.code == 'IRSA':
                        vals['irsa'] = line.total
                    
                for line in data.details_by_salary_rule_category:
                    if line.code == 'OMSI_PAT':
                        vals['omsiemp'] = line.total
                    if line.code == 'CNAPS_PAT':
                        vals['cnapsemp'] = line.total
                    if line.code == 'NET':
                        vals['net'] = line.total
                        
                vals['totalomsi'] = vals.get('omsi', 0.0) + vals.get('omsiemp', 0.0)
                vals['totalcnaps'] = vals.get('cnaps', 0.0) + vals.get('cnapsemp', 0.0)
                self.pool.get('etat.salaire2').write(cr, uid, [data.etat_salaire_id.id], vals, context=context)
                
                #ostie
                vals_ostie = vals.copy()
                not_in_ostie = ['cnaps', 'cnapsemp', 'totalcnaps', 'irsa'] 
                for cle in not_in_ostie:
                    if cle in vals_ostie:
                        del vals_ostie[cle]
                self.pool.get('ostie').write(cr, uid, [data.ostie_id.id], vals_ostie, context=context)
                
                #irsa
                vals_irsa = vals.copy()
                not_in_irsa = ['cnaps', 'cnapsemp', 'totalcnaps', 'omsi', 'omsiemp', 'totalomsi'] 
                for cle in not_in_irsa:
                    if cle in vals_irsa:
                        del vals_irsa[cle]
                self.pool.get('irsa2').write(cr, uid, [data.irsa_id.id], vals_irsa, context=context)
                
                #cnaps
                vals_cnaps = vals.copy()
                not_in_cnaps = ['irsa', 'omsi', 'omsiemp', 'totalomsi'] 
                for cle in not_in_cnaps:
                    if cle in vals_cnaps:
                        del vals_cnaps[cle]
                self.pool.get('cnaps2').write(cr, uid, [data.cnaps_id.id], vals_cnaps, context=context)     
                
        return True
    
    def unlink(self, cr, uid, ids, context=None):
        context['forcer_suppresion'] = True
        for data in self.browse(cr, uid, ids, context=context):
            self.pool.get('etat.salaire2').unlink(cr, uid, [data.etat_salaire_id.id], context=context)
            self.pool.get('ostie').unlink(cr, uid, [data.ostie_id.id], context=context)
            self.pool.get('irsa2').unlink(cr, uid, [data.irsa_id.id], context=context)
            self.pool.get('cnaps2').unlink(cr, uid, [data.cnaps_id.id], context=context)
        super(hr_payslip, self).unlink(cr, uid, ids, context=context)