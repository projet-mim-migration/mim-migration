# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
 
class cnaps(osv.osv):
    _name = "cnaps2"
    _description = "Etat CNAPS"
    _columns = {
        'employee_id': fields.many2one('hr.employee',string=u'Employé', readonly=True),
        'num_emp': fields.char('Matricule', size=128, readonly=True),
        'num_cin': fields.char('CIN', size=128, readonly=True),
        'name_related': fields.char('Nom', size=128, readonly=True),
        'basic': fields.float('Salaire de base', readonly=True),
        'cnaps': fields.float('CNAPS Travailleur', readonly=True),
        'cnapsemp': fields.float('CNAPS Employeur', readonly=True),
        'brut': fields.float('Salaire Brut', readonly=True),
        'net': fields.float('Salaire Net', readonly=True),
        'date_from': fields.date('Start Date', readonly=True),
        'date_to': fields.date('End Date', readonly=True),
        'totalcnaps': fields.float('TOTAL CNAPS', readonly=True),
    } 
    _order = 'date_to desc'
    
    def unlink(self, cr, uid, ids, context=None):
        context = context or {}
        if not context.get('forcer_suppresion'):
            raise osv.except_osv('Erreur!', 'Supprimer le bulletin de paie lié pour une suppression')
        super(cnaps, self).unlink(cr, uid, ids, context=context)

