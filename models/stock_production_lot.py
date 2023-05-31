from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta



class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_id = fields.Many2one(
        'product.product', 'Product',
        # domain="[('company_id', '=', company_id)]", check_company=True,
        required=True)

    time_left = fields.Integer('Time Left of Product',
                               compute="count_time_left",
                               store=True)

    @api.depends('expiration_date')
    def count_time_left(self):
        if self.expiration_date is not False:
            current_time = datetime.now().day
            if self.expiration_date.day > current_time:
                self.time_left = (self.expiration_date.day - current_time)
            else:
                self.time_left = -(current_time - self.expiration_date.day)

    def button_scrap_iuh(self):
        self.ensure_one()
        view = self.env.ref('stock.stock_scrap_form_view')
        products = self.env['product.product']
        return {
            'name': _('Scrap'),
            'view_mode': 'form',
            'res_model': 'stock.scrap',
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'type': 'ir.actions.act_window',
            'context': {'product_ids': products.ids, 'default_company_id': self.company_id.id},
            'target': 'new',
        }

    def button_scrap_1_iuh(self):
        self.ensure_one()
        view = self.env.ref('stock.stock_scrap_form_view')
        products = self.env['product.product']
        return {
            'name': _('Scrap'),
            'view_mode': 'form',
            'res_model': 'stock.scrap',
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'type': 'ir.actions.act_window',
            'context': {'product_ids': products.ids,
                        'default_company_id': self.company_id.id},
            'target': 'new',
        }
    def button_return_iuh(self):
        self.ensure_one()
        view = self.env.ref('stock.view_picking_form')
        products = self.env['product.product']
        return {
            'name': _('Returned Picking'),
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'product_ids': products.ids,
                        'default_company_id': self.company_id.id},
        }