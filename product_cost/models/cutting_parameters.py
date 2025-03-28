from odoo import models,fields, api
from odoo.tools.populate import compute


class cutting_parameters(models.Model):
    _name = 'cutting.parameters'
    _description = 'Parametros de corte'

    #product_id = fields.Many2one('product.product', string="Producto", required=True)
    product_id = fields.Many2one(
        'product.template', string="Producto", required=True
    )

    product_variant_id = fields.Many2one(
        'product.product', string="Variante del Producto",
        domain="[('product_tmpl_id', '=', product_id)]"
    )

    separation  = fields.Float(String="Separacion", digit=(10, 2), default=0.0, required=True)
    process = fields.Many2one('process.type.parameters', string="Proceso", required=True)
    color = fields.Integer(String = "Color", required=True)
    speed = fields.Float(String="Velocidad", digit=(10, 2), default=0.0, required=True)
    maximum_power = fields.Float(String="Poder maximo", digit=(10, 2), default=0.0, required=True)
    minimum_power = fields.Float(String="Poder minimo", digit=(10, 2), default=0.0, required=True)
    number_passed = fields.Integer(String = "Numero de pasadas", required=True)

