from odoo import models, fields


class Department(models.Model):
    _name = 'hms.department'
    # _rec_name = 'Capacity'
    _rec_name = 'Name'

    Name = fields.Char()
    is_opened = fields.Boolean()
    Capacity = fields.Integer()
    patient_ids = fields.One2many('hms.patient', 'department_name_id')
