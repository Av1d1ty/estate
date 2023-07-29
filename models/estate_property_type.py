from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property type'
    _order = 'name desc'

    name = fields.Char("Title", required=True)
    active = fields.Boolean(default=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many(related='property_ids.offer_ids')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'Types must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
