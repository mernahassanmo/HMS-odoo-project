from odoo import fields, models


class log_history(models.Model):
    _name = 'hms.log.history'
    _rec_name = 'created_by'

    created_by = fields.Char()
    Date = fields.Date()
    Description = fields.Text()
    patient_id = fields.Many2one('hms.patient')

    # patient_id = fields.One2many('hms.patient', 'log_history_id')
