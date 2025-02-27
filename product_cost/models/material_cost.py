from odoo import models,fields, api
from odoo.exceptions import UserError


class material_cost(models.Model):
    _name = 'material.cost'
    _description = 'Costo de Material'


    product_id = fields.Many2one('product.product', string="Producto", required=True)
    unit_cost = fields.Float(string="Costo",related='product_id.product_tmpl_id.standard_price', store=True,readonly=True)
    quantity = fields.Float(String="Cantidad", digit=(10, 2), default=0.0)
    uom_id = fields.Many2one(
        'uom.uom',
        string="Unidad",
        related='product_id.uom_id',
        store=True,
        readonly=True
    )
    material_cost = fields.Float(String="Total", digit=(10, 2), default=0.0, compute="_compute_total_cost")
    product_cost_id =  fields.Many2one('product.cost', string="Producto costo", required=True)

    @api.depends('unit_cost', 'quantity')
    def _compute_total_cost(self):
        for record in self:
            record.material_cost = record.unit_cost * record.quantity



