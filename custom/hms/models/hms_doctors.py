from odoo import models, fields


class Doctor(models.Model):
    _name = 'hms.doctors'
    _rec_name = 'First_name'

    First_name = fields.Char()
    Last_name = fields.Char()
    image = fields.Image()
