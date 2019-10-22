# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    def _compute_dimension_uom_name(self):
        for template in self:
            template.dimension_uom_name = self.env['product.template']\
                ._get_dimension_uom_name_from_ir_config_parameter()

    @api.onchange('length', 'height', 'width')
    def onchange_calculate_volume(self):
        self.volume = self.env['product.template']._calc_volume(
            self.length, self.height, self.width)

    length = fields.Float()
    height = fields.Float()
    width = fields.Float()
    dimension_uom_name = fields.Char(
        string='Dimension unit of measure label',
        compute='_compute_dimension_uom_name',
        default=_compute_dimension_uom_name
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_dimension_uom_name(self):
        for template in self:
            template.dimension_uom_name = self._get_dimension_uom_name_from_ir_config_parameter()

    def _get_dimension_uom_name_from_ir_config_parameter(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        return "ft" if get_param('product.volume_in_cubic_feet') == '1' else "m"

    def _calc_volume(self, length, height, width):
        # Get product volume config setting
        volume = 0
        if length and height and width:
            volume = length * height * width

        return volume

    @api.onchange('length', 'height', 'width')
    def onchange_calculate_volume(self):
        self.volume = self._calc_volume(
            self.length, self.height, self.width)

    length = fields.Float(store=True, related='product_variant_ids.length')
    height = fields.Float(store=True, related='product_variant_ids.height')
    width = fields.Float(store=True, related='product_variant_ids.width')
    dimension_uom_name = fields.Char(related='product_variant_ids.dimension_uom_name')

class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    length = fields.Float()
    height = fields.Float()
    width = fields.Float()
    dimension_uom_name = fields.Char(related='product_id.dimension_uom_name')
