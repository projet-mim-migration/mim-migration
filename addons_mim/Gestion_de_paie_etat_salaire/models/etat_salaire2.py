# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api

 
class EtatSalaire2(models.Model):
    _name = "etat.salaire2"
    _description = "Etat global des salaires"
    
    employee_id = fields.Many2one(
        'hr.employee',
        string=u'Employé', 
        readonly=True
    )
    num_emp = fields.Char(
        'Matricule', 
        size=128, 
        readonly=True
    )
    num_cin = fields.Char(
        'CIN', 
        size=128, 
        readonly=True
    )
    name_related = fields.Char(
        'Nom', 
        size=128, 
        readonly=True
    )
    basic = fields.Float(
        'Salaire de base', 
        readonly=True
    )
    omsi = fields.Float(
        'OMSI Travailleur', 
        readonly=True
    )
    omsiemp = fields.Float(
        'OMSI Employeur', 
        readonly=True
    )
    cnaps = fields.Float(
        'CNAPS Travailleur', 
        readonly=True
    )
    cnapsemp = fields.Float(
        'CNAPS Employeur', 
        readonly=True
    )
    brut = fields.Float(
        'Salaire Brut', 
        readonly=True
    )
    irsa = fields.Float(
        'IRSA', 
        readonly=True
    )
    net = fields.Float(
        'Salaire Net', 
        readonly=True
    )
    date_from = fields.Date(
        'Start Date', 
        readonly=True
    )
    date_to = fields.Date(
        'End Date', 
        readonly=True
    )
    totalcnaps = fields.Float(
        'TOTAL CNAPS', 
        readonly=True
    )
    totalomsi = fields.Float(
        'TOTAL OMSI', 
        readonly=True
    )
    
    _order = 'date_to desc'
    
    @api.multi
    def unlink(self):
        context = self._context or {}
        if not context.get('forcer_suppresion'):
            raise exceptions.UserError('Supprimer le bulletin de paie lié pour une suppression')
        super(EtatSalaire2, self).unlink()

