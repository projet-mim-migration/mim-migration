
from openerp.osv import osv
from openerp.osv import fields
import openerp.addons.decimal_precision as dp

class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'
    
    _columns = {
     'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price'), readonly=True),
    }
sale_order_line()    