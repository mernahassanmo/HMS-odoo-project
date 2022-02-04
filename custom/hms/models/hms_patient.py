from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class patient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'First_name'

    First_name = fields.Char()
    Last_name = fields.Char()
    Email = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b-', 'B-'), ('b+', 'B+')])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Char()
    age = fields.Integer()

    doctor_name_id = fields.Many2many('hms.doctors')
    department_name_id = fields.Many2one('hms.department')
    capacity = fields.Integer(related='department_name_id.Capacity')
    log_history_id = fields.One2many('hms.log.history', 'patient_id')

    # log_history_id = fields.Many2one('hms.log.history')

    @api.onchange('Email')
    def validate_mail(self):
        if self.Email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.Email)
            if match == None:
                raise ValidationError('Not a valid E-mail ')

    # _sql_constraints = [
    #     # ('constraint name', 'constraint type', 'message ')
    #     ('unique_email', 'UNIQUE(Email)', 'Email must be unique.'),
    #
    # ]

    @api.model
    def create(self, vals_list):
        if not vals_list['Email']:
            vals_list['Email'] = f"{vals_list['First_name']}@gmail.com"
        patient = self.search([('Email', '=', vals_list['Email'])])
        if patient:
            raise UserError(f"{vals_list['Email']} already exists")

        return super().create(vals_list)

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.birth_date:
            self.age = date.today().year - self.birth_date.year

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    def next_stage(self):
        if self.state == 'undetermined':
            self.state = 'good'
        elif self.state == 'good':
            self.state = 'fair'
        elif self.state == 'fair':
            self.state = 'serious'
        elif self.state == 'serious':
            self.state = 'undetermined'
        self.create_log()

    def create_log(self):

        self.env['hms.log.history'].create({
            'created_by': self.First_name,
            'Date': date.today(),
            'Description': f'State changed to {self.state} ',
            'patient_id': self.id
        })

    @api.onchange('age')
    def pcr_check(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR',
                    'message': 'pcr has been checked.'
                }
            }
