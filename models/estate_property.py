from dateutil.relativedelta import relativedelta
from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'

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
            ('offer_received', 'Offer received'),
            ('offer_accepted', 'Offer accepted'),
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
