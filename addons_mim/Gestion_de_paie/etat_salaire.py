from openerp.osv import fields,osv
from openerp import tools
 
class etat_salaire(osv.osv):
    _name = "etat.salaire"
    _description = "etat global salaire"
    _auto = False
    _columns = {
	    'id': fields.char('ID', size=128, readonly=True),
		'num_emp': fields.char('Matricule', size=128, readonly=True),
		'num_cin': fields.char('CIN', size=128, readonly=True),
        'name_related': fields.char('Nom', size=128, readonly=True),
        'basic': fields.float('Salaire de base', readonly=True),
        'omsi': fields.float('OMSI Travailleur', readonly=True),
		'omsiemp': fields.float('OMSI Employeur', readonly=True),
        'cnaps': fields.float('CNAPS Travailleur', readonly=True),
		'cnapsemp': fields.float('CNAPS Employeur', readonly=True),
		'brut': fields.float('Salaire Brut', readonly=True),
        'irsa': fields.float('IRSA', readonly=True),
        'net': fields.float('Salaire Net', readonly=True),
        'date_from': fields.date('Start Date', readonly=True),
        'date_to': fields.date('End Date', readonly=True),
        'totalcnaps': fields.float('TOTAL CNAPS', readonly=True),
        'totalomsi': fields.float('TOTAL OMSI', readonly=True),

    } 
    _order = 'num_emp asc'
 
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'etat_salaire')
        cr.execute("""
            CREATE OR REPLACE VIEW etat_salaire AS (
                select p.employee_id as id,date_from,date_to,emp.num_emp,emp.num_cin,emp.num_cnaps_emp,
                emp.name_related,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='BASIC') as basic,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_EMP')as omsi,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_PAT')as omsiemp,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_EMP')+(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_PAT')as totalomsi,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_EMP')as cnaps,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_PAT')as cnapsemp,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_EMP')+(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_PAT')as totalcnaps,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='GROSS')as brut,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='IRSA')as irsa,
                (select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='NET')as net
                 from hr_payslip p inner join hr_employee emp on p.employee_id=emp.id 
            )
        """)
etat_salaire()