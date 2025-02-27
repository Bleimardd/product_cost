from odoo import models,fields, api

class operating_cost(models.Model):
    _name = 'operating.cost'
    _description = 'Costo de operacion'


    product_id = fields.Many2one('product.product', string="Producto", required=True)
    sales_price = fields.Float(string="Precio", related='product_id.product_tmpl_id.list_price', store=True,
                               readonly=True)
    quantity_time = fields.Integer(string="Tiempo")
    uom_id = fields.Many2one(
        'uom.uom',
        string="Unidad",
        related='product_id.uom_id',
        store=True,
        readonly=True
    )

    total = fields.Float(String="Total", digit=(10, 2), default=0.0, compute="_compute_total_cost")
    operating_cost_id = fields.Many2one('product.cost', string="Costo de operacion", required=True)


    @api.depends('sales_price', 'quantity_time')
    def _compute_total_cost(self):
        for record in self:
            record.total = record.sales_price * record.quantity_time