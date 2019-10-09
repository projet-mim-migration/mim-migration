from openerp.report import report_sxw

class irsa_parser(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context):
		super(irsa_parser, self).__init__(cr, uid, name, context)
		self.localcontext.update({
			'time':time,
			'get_irsa': self.get_irsa,
			'get_total_by_rule_category': self.get_total_by_rule_category,
			'get_payslip_lines': self.get_payslip_lines,
		})

	def get_payslip_lines(self, objs):
		payslip_line = self.pool.get('hr.payslip.line')
		res = []
		ids = []
		for item in objs:
			ids.append(item.id)
		if ids:
			res = payslip_line.browse(self.cr, self.uid, ids)
		return res

	def get_total_by_rule_category(self, obj, code):
		payslip_line = self.pool.get('hr.payslip.line')
		rule_cate_obj = self.pool.get('hr.salary.rule.category')

		cate_ids = rule_cate_obj.search(self.cr, self.uid, [('code', '=', code)])

		category_total = 0
		if cate_ids:
			line_ids = payslip_line.search(self.cr, self.uid, [('slip_id', '=', obj.id),('category_id.id', '=', cate_ids[0] )])
		for line in payslip_line.browse(self.cr, self.uid, line_ids):
			category_total += line.total

		return category_total


	def get_irsa(self,objs):
		#sql=""" select id,num_emp,num_cin,name_related,basic,omsi,omsiemp,cnaps,cnapsemp,brut,irsa,net,date_from,date_to,totalcnaps,totalomsi from etat_salaire		
		#sql="""select p.employee_id as id,date_from,date_to,emp.num_emp,emp.num_cin,emp.num_cnaps_emp,emp.name_related,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='BASIC') as basic,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_EMP')as omsi,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_PAT')as omsiemp,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_EMP')as cnaps,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_PAT')as cnapsemp,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='GROSS')as brut,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='IRSA')as irsa,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='NET')as net from hr_payslip p inner join hr_employee emp on p.employee_id=emp.id
		sql="""select id,num_emp,num_cin,name_related,basic,brut,irsa,net,date_from,date_to from irsa 
		
		) """
		self.cr.execute(sql)
		res=self.cr.dictfetchall()
		return res


report_sxw.report_sxw('report.etat.irsa', 'irsa', 'Gestion_de_paie/report/rapport_irsa.rml', parser=irsa_parser)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

