# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    
    etat_salaire_id = fields.Many2one(
        'etat.salaire2',
        string='Etat salaire'
    )
    ostie_id = fields.Many2one(
        'ostie',
        string='Etat OSTIE'
    )
    irsa_id = fields.Many2one(
        'irsa2',
        string='Etat IRSA'
    )
    cnaps_id = fields.Many2one(
        'cnaps2',
        string='Etat CNAPS'
    )
    
    @api.model
    def create(self, vals):
        payslip_id = super(HrPayslip, self).create(vals)
        data = self.env['hr.payslip'].browse(payslip_id.id)
        vals = {
                'employee_id': data.employee_id.id,
                'num_emp': data.employee_id.num_emp,
                'num_cin': data.employee_id.num_cin,
                'name_related': data.employee_id.name,
                'date_from': data.date_from,
                'date_to': data.date_to,
                }
        etat_id = self.env['etat.salaire2'].create(vals)
        ostie_id = self.env['ostie'].create(vals)
        irsa_id = self.env['irsa2'].create(vals)
        cnaps_id = self.env['cnaps2'].create(vals)
        data.write({
            'etat_salaire_id': etat_id.id, 
            'ostie_id': ostie_id.id, 
            'irsa_id': irsa_id.id, 
            'cnaps_id': cnaps_id.id,
        })
        
        return payslip_id

    @api.multi
    def write(self, vals):
        super(HrPayslip, self).write(vals)
        for data in self:
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
                self.env['etat.salaire2'].search([('id', '=', data.etat_salaire_id.id)]).write(vals)
                
                #ostie
                vals_ostie = vals.copy()
                not_in_ostie = ['cnaps', 'cnapsemp', 'totalcnaps', 'irsa']
                for cle in not_in_ostie:
                    if cle in vals_ostie:
                        del vals_ostie[cle]
                self.env['ostie'].search([('id', '=', data.ostie_id.id)]).write(vals_ostie)
                
                #irsa
                vals_irsa = vals.copy()
                not_in_irsa = ['cnaps', 'cnapsemp', 'totalcnaps', 'omsi', 'omsiemp', 'totalomsi'] 
                for cle in not_in_irsa:
                    if cle in vals_irsa:
                        del vals_irsa[cle]
                self.env['irsa2'].search([('id', '=', data.irsa_id.id)]).write(vals_irsa)
                
                #cnaps
                vals_cnaps = vals.copy()
                not_in_cnaps = ['irsa', 'omsi', 'omsiemp', 'totalomsi']
                for cle in not_in_cnaps:
                    if cle in vals_cnaps:
                        del vals_cnaps[cle]
                self.env['cnaps2'].search([('id', '=', data.cnaps_id.id)]).write(vals_cnaps)
                
        return True
    
    @api.multi
    def unlink(self):
        self = self.with_context(forcer_suppresion=True)
        for data in self:
            self.env['etat.salaire2'].search([('id', '=', data.etat_salaire_id.id)]).unlink()
            self.env['ostie'].search([('id', '=', data.ostie_id.id)]).unlink()
            self.env['irsa2'].search([('id', '=', data.irsa_id.id)]).unlink()
            self.env['cnaps2'].search([('id', '=', data.cnaps_id.id)]).unlink()

        super(HrPayslip, self).unlink()