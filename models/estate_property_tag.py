from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"

    name = fields.Char("Title", required=True)
