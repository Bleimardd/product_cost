from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    calculation_use_machinery = fields.Boolean(string="Cálculo por uso de maquinaría")
    use_machinery = fields.Boolean(string="Uso de máquinas y herramientas")
    product_cost_id = fields.Many2one(
        comodel_name='product.template',
        string="Uso de máquinas y herramientas"
    )
    useful_life = fields.Float(String = "Vida util", digit = (10, 2), default = 0.0)


    products_price_ids = fields.Many2many(
        string='Servicios',
        comodel_name='product.template',
        relation='product_template_this_rel',
        column1='original_id',
        column2='servicio_id',
    )


    def accion_calcular_precio(self):
        for record in self:
            if record.useful_life == 0:
                raise UserError("No se puede dividir entre cero.")
            if record.product_cost_id.standard_price  == 0:
                raise UserError("El costo del producto no puede ser cero.")
            record.list_price = record.product_cost_id.standard_price / record.useful_life

    def action_sumar_precios(self):
        """Suma los precios de los productos relacionados y actualiza list_price"""
        for record in self:
            total = sum(record.products_price_ids.mapped('list_price'))
            if total <= 0:
                raise UserError("El total no puede ser 0 o negativo.")
            record.list_price = total
