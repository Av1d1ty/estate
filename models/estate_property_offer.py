from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float()
    status = fields.Selection(copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True)
    property_id = fields.Many2one('estate.property', string='Property',
                                  required=True)
    validity = fields.Integer(string='Validity (days)', default=lambda self: 7)
    date_deadline = fields.Date(compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline',
                                string='Deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            start_date = (record.create_date
                          if record.create_date is not False
                          else fields.Date.today())
            record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = (record.create_date
                          if record.create_date is not False
                          else fields.Date.today())
            record.validity = (record.date_deadline - start_date.date()).days
