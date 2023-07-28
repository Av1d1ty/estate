from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"

    name = fields.Char("Title", required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'Types must be unique.')
    ]
