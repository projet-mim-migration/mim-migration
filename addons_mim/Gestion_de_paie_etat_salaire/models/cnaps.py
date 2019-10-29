# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api


class Cnaps(models.Model):
    _name = "cnaps2"
    _description = "Etat CNAPS"
    
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

    _order = 'date_to desc'
    
    
    @api.multi
    def unlink(self):
        context = self._context or {}
        if not context.get('forcer_suppresion'):
            raise exceptions.UserError('Erreur!', 'Supprimer le bulletin de paie lié pour une suppression')
        super(Cnaps, self).unlink()

