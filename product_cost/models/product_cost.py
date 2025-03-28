# -*- coding: utf-8 -*-
from unittest import result

from cryptography.utils import read_only_property
from odoo import models,fields, api
import logging

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class product_cost(models.Model):
    _name = 'product.cost'

    product_smart_id = fields.Many2one('product.template', string="Producto")
    name = fields.Char(string = "Nombre del producto", required = True)

    stage = fields.Selection(
        selection=[('new', 'Nuevo'),
                   ('approved', 'Aprobado'),
                   ('cancel', 'Cancelado'),
                   ]
    )


    gain_factor = fields.Float(String = "Factor ganancia", digit = (10, 2), default = 1.5)
    product_price = fields.Float( compute="_compute_price_product", String = "Precio del producto", digit = (10, 2), default = 0.0)
    product_total_cost = fields.Float(compute="_compute_product_total_cost", String = "Costo del producto", digit = (10, 2), default = 0.0, readonly = True)

    material_cost_ids = fields.One2many('material.cost', 'product_cost_id', string="Costos de Material")
    total_line_products = fields.Float(String = "Total de materiales", compute="_compute_total_line_products", digit = (10, 2), default = 0.0, readonly = True)

    material_tools_cost_ids = fields.One2many('material.tools.cost', 'material_tools_cost_id', string="Costos de Material y Herramienta")
    total_service_machines_tools = fields.Float( compute="_compute_total_service_machines_tools", String = "Total de servicio de maquinas y herramientas", digit = (10, 2), default = 0.0, readonly = True)


    cutting_cost_ids = fields.One2many('cutting.cost', 'cutting_cost_id', string="Costos de corte")
    total_service_cort = fields.Float(compute="_compute_total_service_cort",String = "Total costo de corte", digit = (10, 2), default = 0.0, readonly = True)


    operating_cost_ids = fields.One2many('operating.cost', 'operating_cost_id', string="Costos de operacion")
    total_operating_cost = fields.Float(compute="_compute_total_operating_cost",String = "Total costo de operacion", digit = (10, 2), default = 0.0, readonly = True)



    def action_view_product(self):
        self.ensure_one()
        if self.product_smart_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Producto',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': self.product_smart_id.id,
                'target': 'current',
            }


    def action_create_product(self):
        productsearch = self.env['product.product'].search([('name', '=', self.name)], limit=1)
        mto_route = self.env['stock.route'].with_context(active_test=False).search([('id', '=', 1)])
        fab_id = self.env.ref('mrp.route_warehouse0_manufacture').id
        #mto_route.active = True

        
        _logger.info(mto_route)
        _logger.info(fab_id)
      

        if not productsearch:

            new_product = self.env['product.template'].create({
                'name': self.name,
                'sale_ok': True,
                'purchase_ok': False,
                'type': 'product',
                'invoice_policy': 'order',
                'uom_id': 1,
                'list_price': self.product_price,
                'standard_price': self.product_total_cost,
                'route_ids': [(6, 0, [mto_route.id,fab_id])],
            })



            product_id = new_product.id

            for record in self:
                record.write({'product_smart_id': product_id})

                _logger.info(f"El producto se : {product_id}")

                mrp = self.env['mrp.bom'].create({
                    'product_tmpl_id': product_id,
                    'product_qty': 1,
                    'type': 'normal',

                })


                if self.material_cost_ids:
                    for material_ids in self.material_cost_ids:
                        mrp_lines = self.env['mrp.bom.line'].create({
                            'bom_id': mrp.id,
                            'product_id': material_ids.product_id.id,
                            'product_qty': material_ids.quantity,
                        })

                if self.material_tools_cost_ids:
                    for tools_cost_ids in self.material_tools_cost_ids:
                        mrp_lines = self.env['mrp.bom.line'].create({
                            'bom_id': mrp.id,
                            'product_id': tools_cost_ids.product_id.id,
                            'product_qty': 1,
                        })

                if self.cutting_cost_ids:
                    for cutting_ids in self.cutting_cost_ids:
                        mrp_lines = self.env['mrp.bom.line'].create({
                            'bom_id': mrp.id,
                            'product_id': cutting_ids.product_id.id,
                            'product_qty': cutting_ids.time,
                        })



                if self.operating_cost_ids:
                    for operating_ids in self.operating_cost_ids:
                        mrp_lines = self.env['mrp.bom.line'].create({
                            'bom_id': mrp.id,
                            'product_id': operating_ids.product_id.id,
                            'product_qty': operating_ids.quantity_time,
                        })


        else:
            raise UserError("Ya existe el producto con el  mismo nombre")



        return




    #---------------------------------
    def action_update_product(self):

        # _logger.info(f"El producto se : {self.product_smart_id}")
        # print(self.product_smart_id.id)
        products = self.env['product.template'].search([('id', '=', self.product_smart_id.id)])

        products.write({'standard_price': self.product_total_cost, 'list_price': self.product_price})

        bom_records = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_smart_id.id)])

        bom_lines_records = self.env['mrp.bom.line'].search([('bom_id', '=', bom_records.id)])

        if bom_lines_records:
            bom_lines_records.unlink()


        if self.material_cost_ids:
            for material_ids in self.material_cost_ids:
                bom_records.write({
                    'bom_line_ids': [(0, 0, {
                    'product_id': material_ids.product_id.id,
                    'product_qty': material_ids.quantity,
                    })]
                })

        if self.material_tools_cost_ids:
            for tools_cost_ids in self.material_tools_cost_ids:
                bom_records.write({
                    'bom_line_ids': [(0, 0, {
                        'product_id': tools_cost_ids.product_id.id,
                        'product_qty': 1,
                    })]
                })

        if self.cutting_cost_ids:
            for cutting_ids in self.cutting_cost_ids:
                bom_records.write({
                    'bom_line_ids': [(0, 0, {
                        'product_id': cutting_ids.product_id.id,
                        'product_qty': cutting_ids.time,
                    })]
                })

        if self.operating_cost_ids:
            for operating_ids in self.operating_cost_ids:
                bom_records.write({
                    'bom_line_ids': [(0, 0, {
                        'product_id': operating_ids.product_id.id,
                        'product_qty': operating_ids.quantity_time,
                    })]
                })

        return




    @api.depends('material_cost_ids')
    def _compute_total_line_products(self):
        for record in self:
            record.total_line_products = sum(record.material_cost_ids.mapped('material_cost'))

    @api.depends('material_tools_cost_ids')
    def _compute_total_service_machines_tools(self):
        for record in self:
         record.total_service_machines_tools  = sum(record.material_tools_cost_ids.mapped('sales_price'))

    @api.depends('cutting_cost_ids')
    def _compute_total_service_cort(self):
        for record in self:
            record.total_service_cort = sum(record.cutting_cost_ids.mapped('total'))

    @api.depends('operating_cost_ids')
    def _compute_total_operating_cost(self):
        for record in self:
            record.total_operating_cost = sum(record.operating_cost_ids.mapped('total'))

    @api.depends('total_line_products','total_service_machines_tools','total_service_cort','total_operating_cost')
    def _compute_product_total_cost(self):
        for record in self:
            record.product_total_cost = record.total_line_products + record.total_service_machines_tools + record.total_service_cort + record.total_operating_cost

    @api.depends('product_total_cost','gain_factor')
    def _compute_price_product(self):
        for record in self:
            record.product_price = record.product_total_cost * (1+ record.gain_factor)

    @api.model
    def create(self, vals):

        vals.setdefault('stage', 'new')

        # Creamos el registro normalmente
        record = super(product_cost, self).create(vals)

        # Si no hay registros en material_tools_cost_ids, agregamos uno por defecto
        if not record.material_tools_cost_ids:
            record.material_tools_cost_ids = [(0, 0, {
                'product_id': 124
            })]

        if not record.cutting_cost_ids:
            record.cutting_cost_ids = [
                (0, 0, {'product_id': 126}),
                (0, 0, {'product_id': 125})
            ]

        if not record.operating_cost_ids:
            record.operating_cost_ids = [
                (0, 0, {'product_id': 105}),
                (0, 0, {'product_id': 109}),
                (0, 0, {'product_id': 128}),
                (0, 0, {'product_id': 110}),

                (0, 0, {'product_id': 106}),
                (0, 0, {'product_id': 111})
            ]

        return record

    #@api.model
    def write(self, vals):
        resultado = super(product_cost, self).write(vals)
        self.action_update_product()
        return resultado


    product_id = fields.Many2one('product.product', string="Producto")
    is_product_created = fields.Boolean(compute="_compute_is_product_created", store=True)

    #@api.depends('product_id')
    def _compute_is_product_created(self):
        #productsearch = self.env['product.product'].search([('name', '=', self.name)], limit=1)
        print("HEEEEEEEEEEEEEREEEEEEEEE")
        for record in self:
            record.is_product_created = bool(record.product_id)
            print("*  ", record.is_product_created)



