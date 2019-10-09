from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

#modif
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from openerp import tools

from openerp.tools.translate import _

#(on ajoute ce qui sont utile pour la loi salariale malgache )
#herite du classe hr.contract
class hr_contract(osv.osv):
    _inherit = 'hr.contract'

    _columns = {
        'categorie': fields.char('Categorie Professionnel', size=64),
        'echellon': fields.char('Echellon', size=64),
        'indice': fields.integer('Indice', size=10),
        'horaire_hebdo': fields.float('Horaire hébdomadaire',digits_compute=dp.get_precision('Payroll')),
        'payment_mode': fields.selection([('VIREMENT', 'VIREMENT'),('ESPECE', 'ESPECE')], 'Mode de paiement'),
    }
hr_contract()


#herite du classe res.company
class res_company(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'seuil_irsa': fields.float('Seuil IRSA', digits_compute=dp.get_precision('Payroll')),
        'taux_irsa': fields.float('Taux IRSA', digits_compute=dp.get_precision('Payroll')),
        'abat_irsa': fields.float('Abattement IRSA', digits_compute=dp.get_precision('Payroll')),
        'cotisation_cnaps_patr': fields.float('Cotisation Patronale CNAPS', digits_compute=dp.get_precision('Payroll')),
        'cotisation_cnaps_emp': fields.float('Cotisation Employé CNAPS', digits_compute=dp.get_precision('Payroll')),
        'plafond_cnaps': fields.float('Plafond de la Securite Sociale', digits_compute=dp.get_precision('Payroll')),
        'num_cnaps_patr': fields.char('N° CNAPS', size=64),
        'cotisation_sante_patr': fields.float('Cotisation Patronale Santé', digits_compute=dp.get_precision('Payroll')),
        'cotisation_sante_emp': fields.float('Cotisation Employé Santé', digits_compute=dp.get_precision('Payroll')),
        'org_sante': fields.char('Organisme sanitaire', size=64),
        'conge_mens': fields.float('Nombre de jour congé mensuel', digits_compute=dp.get_precision('Payroll')),
    }

res_company()


#herite de hr.employee
class hr_employee(osv.osv):
    _inherit = 'hr.employee'    
    _columns = {
        'num_cnaps_emp':fields.char('N° CNAPS', size=64),
        'num_emp':fields.char('N° Matricule', size=64),
        'num_cin':fields.char('N° CIN', size=64),
    }
hr_employee()

class hr_payslip(osv.osv):
    _inherit = 'hr.payslip'
    
    def onchange_employee_id(self, cr, uid, ids, date_from, date_to, employee_id=False, contract_id=False, context=None):
        empolyee_obj = self.pool.get('hr.employee')
        contract_obj = self.pool.get('hr.contract')
        worked_days_obj = self.pool.get('hr.payslip.worked_days')
        input_obj = self.pool.get('hr.payslip.input')

        if context is None:
            context = {}
        #delete old worked days lines
        old_worked_days_ids = ids and worked_days_obj.search(cr, uid, [('payslip_id', '=', ids[0])], context=context) or False
        if old_worked_days_ids:
            worked_days_obj.unlink(cr, uid, old_worked_days_ids, context=context)

        #delete old input lines
        old_input_ids = ids and input_obj.search(cr, uid, [('payslip_id', '=', ids[0])], context=context) or False
        if old_input_ids:
            input_obj.unlink(cr, uid, old_input_ids, context=context)


        #defaults
        res = {'value':{
                      'line_ids':[],
                      'input_line_ids': [],
                      'worked_days_line_ids': [],
                      #'details_by_salary_head':[], TODO put me back
                      'name':'',
                      'contract_id': False,
                      'struct_id': False,
                      }
            }
        if (not employee_id) or (not date_from) or (not date_to):
            return res
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(date_from, "%Y-%m-%d")))
        employee_id = empolyee_obj.browse(cr, uid, employee_id, context=context)
        res['value'].update({
                    'name': _('Salary Slip of %s for %s') % (employee_id.name, tools.ustr(ttyme.strftime('%B-%Y'))),
                    'company_id': employee_id.company_id.id
        })

        if not context.get('contract', False):
            #fill with the first contract of the employee
            contract_ids = self.get_contract(cr, uid, employee_id, date_from, date_to, context=context)
        else:
            if contract_id:
                #set the list of contract for which the input have to be filled
                contract_ids = [contract_id]
            else:
                #if we don't give the contract, then the input to fill should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, employee_id, date_from, date_to, context=context)

        if not contract_ids:
            return res
        contract_record = contract_obj.browse(cr, uid, contract_ids[0], context=context)
        res['value'].update({
                    'contract_id': contract_record and contract_record.id or False
        })
        struct_record = contract_record and contract_record.struct_id or False
        if not struct_record:
            return res
        res['value'].update({
                    'struct_id': struct_record.id,
        })
        #computation of the salary input
        worked_days_line_ids = self.get_worked_day_lines(cr, uid, contract_ids, date_from, date_to, context=context)
        input_line_ids = self.get_inputs(cr, uid, contract_ids, date_from, date_to, context=context)
        res['value'].update({
                    'worked_days_line_ids': worked_days_line_ids,
                    'input_line_ids': input_line_ids,
        })
        #ando modif
        for w in worked_days_line_ids :
            code1 = w['code']
            contract_id1 = w['contract_id']
            sequence1 = w['sequence']
            nd = w['number_of_days']
            nh = w['number_of_hours']
            name1 = w['name']
            
            res['value'].update({
                        'worked_days_line_ids': [
                             {'code': code1, 'contract_id': contract_id1, 'sequence': sequence1, 'number_of_days': nd, 'number_of_hours': nh, 'name': u''+name1},
                             {'code': 'HS1', 'contract_id': contract_record and contract_record.id or False, 'sequence': 3, 'number_of_days': 0.00, 'number_of_hours': 0.00, 'name': u'Heure supplémentaire 1'},
                             {'code': 'HS2', 'contract_id': contract_record and contract_record.id or False, 'sequence': 4, 'number_of_days': 0.00, 'number_of_hours': 0.00, 'name': u'Heure supplémentaire 2'},
                             {'code': 'HMNUIT', 'contract_id': contract_record and contract_record.id or False, 'sequence': 5, 'number_of_days': 0.00, 'number_of_hours': 0.00, 'name': u'Heure majoré nuit'},
                             {'code': 'HMDIM', 'contract_id': contract_record and contract_record.id or False, 'sequence': 6, 'number_of_days': 0.00, 'number_of_hours': 0.00, 'name': u'Heure majoré dimanche'},
                             {'code': 'HMJF', 'contract_id': contract_record and contract_record.id or False, 'sequence': 7, 'number_of_days': 0.00, 'number_of_hours': 0.00, 'name': u'Heure majoré jour férié'}
                     ],
            })
        
        res['value'].update({
                                     'input_line_ids':[
                        {'code': 'AVANCE15', 'contract_id': contract_record and contract_record.id or False, 'sequence': 1, 'amount': 0.00, 'name': u'Avance quinzaine'},
                        {'code': 'AVANCESP', 'contract_id': contract_record and contract_record.id or False, 'sequence': 2, 'amount': 0.00, 'name': u'Avance spécial'},
                        {'code': 'PRM', 'contract_id': contract_record and contract_record.id or False, 'sequence': 3, 'amount': contract_record and contract_record.type_id and contract_record.type_id.val_prime or 0.00, 'name': u'Prime'},
                        {'code': 'AUTRES', 'contract_id': contract_record and contract_record.id or False, 'sequence': 4, 'amount': 0.00, 'name': u'Autres retenues'}
                                                       ],
                                     })    
        return res

hr_payslip()