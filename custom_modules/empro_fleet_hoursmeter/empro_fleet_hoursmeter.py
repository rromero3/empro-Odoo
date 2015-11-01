from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta

def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)

class fleet_vehicle_hoursmeter(osv.Model):
    _name='fleet.vehicle.hoursmeter'
    _description='Hoursmeter log for a vehicle'
    _order='date desc'

    def _vehicle_log_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            name = record.vehicle_id.name
            if not name:
                name = record.date
            elif record.date:
                name += ' / '+ record.date
            res[record.id] = name
        return res

    def on_change_vehicle(self, cr, uid, ids, vehicle_id, context=None):
        if not vehicle_id:
            return {}

    _columns = {
        'name': fields.function(_vehicle_log_name_get_fnc, type="char", string='Name', store=True),
        'date': fields.date('Date'),
        'value': fields.float('Hoursmeter Value', group_operator="max"),
        'notes': fields.text('Notes'),
        'vehicle_id': fields.many2one('fleet.vehicle', 'Vehicle', required=True)
    }
    _defaults = {
        'date': fields.date.context_today,
    }