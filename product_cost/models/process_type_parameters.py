from odoo import models,fields, api
from odoo.tools.populate import compute


class process_type_parameters(models.Model):
    _name = 'process.type.parameters'
    _description = 'Parametros de tipo de proceso'
    _rec_name = 'type_process_name'

    type_process_name = fields.Char(String="Tipo de proceso", required = True)




