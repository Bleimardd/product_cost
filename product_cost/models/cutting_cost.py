from odoo import models,fields, api
from odoo.tools.populate import compute


class cutting_cost(models.Model):
    _name = 'cutting.cost'
    _description = 'Costo de corte'

    product_id = fields.Many2one('product.product', string="Producto", required=True)
    time = fields.Integer(string="Tiempo")
    price = fields.Float(String="Precio", digit=(10, 2), default=0.0, related='product_id.product_tmpl_id.list_price', store=True,
                             readonly=True)
    uom_id = fields.Many2one(
        'uom.uom',
        string="Unidad",
        related='product_id.uom_id',
        store=True,
        readonly=True
    )
    total = fields.Float(String="Total", digit=(10, 2), default=0.0, compute="_compute_total_cost")
    cutting_cost_id =  fields.Many2one('product.cost', string="Costo de corte", required=True)

    @api.depends('price', 'time')
    def _compute_total_cost(self):
        for record in self:
            record.total = record.price * record.time



