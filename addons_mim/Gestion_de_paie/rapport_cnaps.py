#!/usr/bin/env python
#-*- coding:utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C)Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.report import report_sxw

class cnaps_parser(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context):
		super(cnaps_parser, self).__init__(cr, uid, name, context)
		self.localcontext.update({
		'get_payslip_lines': self.get_payslip_lines,
		'get_total_by_rule_category': self.get_total_by_rule_category,
		'get_employer_line': self.get_employer_line,
		'get_cnaps': self.get_cnaps,
		
		'get_num_cnaps_patr':self.get_num_cnaps_patr,
		'get_name':self.get_name,
		'get_siret':self.get_siret,
		'get_street':self.get_street,
		'get_street2':self.get_street2,
		'get_email':self.get_email,
		'get_plafond_cnaps':self.get_plafond_cnaps,
		
		})

	def get_payslip_lines(self, objs):
		payslip_line = self.pool.get('hr.payslip.line')
		res = []
		ids = []
		for item in objs:
			if item.appears_on_payslip == True and not item.salary_rule_id.parent_rule_id :
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


	def get_cnaps(self):
		#sql=""" select id,date_from,date_to,num_emp,num_cin,num_cnaps_emp,basic,cnapsemp,cnaps,name_related,omsi,omsiemp,brut,irsa,net from etat_salaire 
		if len(self.ids)>1 :
			ids=tuple(self.ids)
			sql="""select p.employee_id as id,date_from,date_to,emp.num_emp,emp.num_cin,emp.num_cnaps_emp,emp.name_related,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='BASIC') as basic,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_EMP')as omsi,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_PAT')as omsiemp,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_EMP')as cnaps,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_PAT')as cnapsemp,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='GROSS')as brut,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='IRSA')as irsa,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='NET')as net 
			from hr_payslip p inner join hr_employee emp on p.employee_id=emp.id
			where (date_from > (select date_start_filter from filter_cnaps where id=(select max(id) from filter_cnaps)
			and date_from < (select date_end_filter from filter_cnaps where id=(select max(id) from filter_cnaps))
				)) and p.employee_id IN {0}""".format(ids)
		else :
			id=self.ids[0]
			sql="""select p.employee_id as id,date_from,date_to,emp.num_emp,emp.num_cin,emp.num_cnaps_emp,emp.name_related,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='BASIC') as basic,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_EMP')as omsi,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_PAT')as omsiemp,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_EMP')as cnaps,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_PAT')as cnapsemp,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='GROSS')as brut,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='IRSA')as irsa,
			(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='NET')as net 
			from hr_payslip p inner join hr_employee emp on p.employee_id=emp.id
			where (date_from > (select date_start_filter from filter_cnaps where id=(select max(id) from filter_cnaps)
			and date_from < (select date_end_filter from filter_cnaps where id=(select max(id) from filter_cnaps))
				)) and p.employee_id = {0}""".format(id)
		#p.employee_id				
		self.cr.execute(sql)
		res=self.cr.dictfetchall()
		return res

	def get_num_cnaps_patr(self):
		sql = "select res_company.num_cnaps_patr from hr_payslip inner join res_company on hr_payslip.company_id = res_company.id"
		self.cr.execute(sql)
		res = self.cr.fetchall()
		return res[0][0]
	def get_name(self):
		sql = "select res_company.name from hr_payslip inner join res_company on hr_payslip.company_id = res_company.id"
		self.cr.execute(sql)
		res = self.cr.fetchall()
		return res[0][0]
	def get_siret(self):
		sql = "select res_company.siret from hr_payslip inner join res_company on hr_payslip.company_id = res_company.id"
		self.cr.execute(sql)
		res = self.cr.fetchall()
		return res[0][0]
	def get_street(self):
		sql = "select res_company.street from hr_payslip inner join res_company on hr_payslip.company_id = res_company.id"
		self.cr.execute(sql)
		res = self.cr.fetchall()
		return res[0][0]
	def get_street2(self):
		sql = "select res_company.street2 from hr_payslip inner join res_company on hr_payslip.company_id = res_company.id"
		self.cr.execute(sql)
		res = self.cr.fetchall()
		print res[0][0]
		return res[0][0]
	def get_email(self):
		sql = "select res_company.email from hr_payslip inner join res_company on hr_payslip.company_id = res_company.id"
		self.cr.execute(sql)
		res = self.cr.fetchall()
		return res[0][0]
	def get_plafond_cnaps(self):
		sql = "select res_company.plafond_cnaps from hr_payslip inner join res_company on hr_payslip.company_id = res_company.id"
		self.cr.execute(sql)
		res = self.cr.fetchall()
		return res[0][0]
	
	def get_employer_line(self, obj, parent_line):

		payslip_line = self.pool.get('hr.payslip.line')

		line_ids = payslip_line.search(self.cr, self.uid, [('slip_id', '=', obj.id), ('salary_rule_id.parent_rule_id.id', '=', parent_line.salary_rule_id.id )])
		res = line_ids and payslip_line.browse(self.cr, self.uid, line_ids[0]) or False

		return res

report_sxw.report_sxw('report.cnaps2', 'hr.payslip', 'Gestion_de_paie/report/rapport_cnaps.rml', parser=cnaps_parser)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
		#sql="""select p.employee_id as id,date_from,date_to,emp.num_emp,emp.num_cin,emp.num_cnaps_emp,emp.name_related,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='BASIC') as basic,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_EMP')as omsi,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='OMSI_PAT')as omsiemp,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_EMP')as cnaps,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='CNAPS_PAT')as cnapsemp,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='GROSS')as brut,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='IRSA')as irsa,(select total from hr_payslip_line pl where pl.slip_id=p.id AND pl.code='NET')as net from hr_payslip p inner join hr_employee emp on p.employee_id=emp.id"""
