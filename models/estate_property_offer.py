from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions


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
    _sql_constraints = [
        ('check_price', 'CHECK (price >= 0)', 'Offer price must be positive.')
    ]

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

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == 'offer_accepted':
                if record.status == 'accepted':
                    raise exceptions.UserError('This offer is already accepted.')
                raise exceptions.UserError('An accepted offer already exists.')
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = self.partner_id
            record.property_id.selling_price = self.price
        return True

    def action_refuse_offer(self):
        for record in self:
            self.status = 'refused'
        return True
