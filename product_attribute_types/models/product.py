# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    is_numeric = fields.Boolean('is_numeric')




class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    is_numeric = fields.Boolean('is_numeric',
                                 related='attribute_id.is_numeric')
    numeric_value = fields.Float('Numeric Value')
    @api.onchange('name')
    def onchange_name(self):
        if self.is_numeric:
            try:
                self.numeric_value = float((''.join([c for c in self.name if c in '1234567890,.'])).replace(',', '.'))
            except Exception:
                pass





    @api.one
    def write(self, vals):
        if vals.get('name',False):
            if  self.is_numeric:
                if vals.get('numeric_value',0.0) == 0.0 or self.numeric_value == 0.00:
                    try:
                        vals['numeric_value'] = float((''.join([c for c in vals.get('name','') if c in '1234567890,.'])).replace(',', '.'))
                    except Exception:
                        pass
        return super(ProductAttributeValue, self).write(vals)

    @api.model
    def create(self, vals):
        create_vals = super(ProductAttributeValue, self).create(vals)
        if vals.get('name',False):
            if create_vals['is_numeric']:
                if create_vals['numeric_value'] == 0.0:
                    try:
                        create_vals['numeric_value'] = float((''.join([c for c in vals.get('name','') if c in '1234567890,.'])).replace(',', '.'))
                    except Exception:
                        pass

        return create_vals
