from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from openerp import fields, models, api

def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)

class empro_employee(osv.osv):
    _inherit = "hr.employee"

    def _get_years(self, cr, uid, ids, hired_years, args, context=None):
        result = dict.fromkeys(ids, 0)
        todays_year= datetime.date.today().year
        for obj in self.browse(cr, uid, ids, context=context):
            start_year = datetime.strptime(obj.start_date, "%Y-%m-%d").date()
            rd = relativedelta(todays_year, start_year)
            result[obj.id] = rd.years

        return result

    _columns = {
        'employee_code': fields.char('Codigo Empro', required=True),
        'legal_name': fields.char('Nombre Legal'),
        'personal_email': fields.char('Email Personal'),
        'personal_phone': fields.char('Telefono Personal'),
        'personal_mobile': fields.char('Celular Personal'),
        'personal_address': fields.char('Direccion Personal'),
        'dependents_count': fields.integer('Numero de Dependientes'),
        'spouse_name': fields.char('Nombre del Conyuge'),
        'emergency_contact': fields.char('Contacto de Emergencia'),
        'driver_license': fields.char('Licencia de Conducir'),
        'driver_license_expiration' : fields.date("Expiracion Licencia de Conducir"),
        'interview_date' : fields.date("Fecha de entrevista"),
        'start_date' : fields.date("Fecha de Inicio", required=True),
        'end_date' : fields.date("Fecha de Salida"),
        'exit_reason': fields.char('Razon de Salida'),
        'years_hired': fields.integer('Anos Contratados'),
        'months_hired': fields.integer('Meses Contratados'),
        'days_hired': fields.integer('Dias Contratados')
    }

    _defaults ={
        'start_date': datetime.date.today()
    }

    @api.onchange('start_date')
    def set_dates_hired(self):
        for rec in self:
            if rec.start_date:
                dt = rec.start_date
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = datetime.date.today()
                rd = relativedelta(d2, d1)
                rec.years_hired = str(rd.years)
                rec.months_hired = str(rd.months)
                rec.days_hired = str(rd.days)

empro_employee()