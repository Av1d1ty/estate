from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'
    _order = 'id desc'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From',
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    state = fields.Selection(required=True, copy=False, default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ]
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesman_id = fields.Many2one('res.users', string='Salesman',
                                  default=lambda self: self._uid)
    offer_ids = fields.One2many('estate.property.offer', 'property_id',
                                string='Offer')
    total_area = fields.Integer(compute='_compute_total_area',
                                string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price',
                              string='Best Offer')

    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price >= 0)', 'Amounts must be positive.'),
        ('check_selling_price', 'CHECK (selling_price >= 0)', 'Amounts must be positive.')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_utils.float_compare(record.selling_price,
                                         record.expected_price * 0.9, 2) == -1:
                raise exceptions.ValidationError(
                    'The selling price must be at least 90% of expected price.')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            if record.living_area != 0 and record.garden_area != 0:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = 0

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if len(record.mapped('offer_ids.price')) > 0:
                record.best_price = max(record.mapped('offer_ids.price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if self.state != 'canceled':
                self.state = 'sold'
            else:
                raise exceptions.UserError('Canceled properties cannot be sold.')
            return True

    def action_cancel(self):
        for record in self:
            if self.state != 'sold':
                self.state = 'canceled'
            else:
                raise exceptions.UserError('Sold properties cannot be canceled.')
            return True
