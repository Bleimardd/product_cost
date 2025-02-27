from odoo import models,fields, api

class material_tools_cost(models.Model):
    _name = 'material.tools.cost'
    _description = 'Costo de Servicio por maquinas y herramientaz'


    product_id = fields.Many2one('product.product', string="Producto", required=True)
    sales_price = fields.Float(string="Precio", related='product_id.product_tmpl_id.list_price', store=True,readonly=True)
    quantity = fields.Float(String="Cantidad", digit=(10, 2), default=0.0)
    uom_id = fields.Many2one('uom.uom', string="Unidad de Medida", related='product_id.uom_id', store=True, readonly=True)
    material_tools_cost_id =  fields.Many2one('product.cost', string="Producto costo", required=True)



