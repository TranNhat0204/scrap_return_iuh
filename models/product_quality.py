from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ProductQuality(models.Model):
    _name = 'product.quality'
    _rec_name = 'product_id'

    product_id = fields.Many2one(
        'product.product', 'Product',
        # domain="[('company_id', '=', company_id)]", check_company=True,
        required=True)
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company, related='product_id.company_id')
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('product_id', '=', product_id)]",
        required=True
        )
    expiration_date = fields.Datetime('Expiration Date',
                                  related='lot_id.expiration_date'
                                  )
    removal_date = fields.Datetime('Removal Date',
                               related='lot_id.removal_date'
                               )
    use_date = fields.Datetime('Use Date',
                           related='lot_id.use_date'
                           )
    alert_date = fields.Datetime('Alert Date',
                             related='lot_id.alert_date'
                             )
    product_qty = fields.Float('Product Quantity',related='lot_id.product_qty')
    product_qty_problem = fields.Float('Number of problem products')
    time_left = fields.Integer('Time Left of Product', compute="count_time_left",store=True)
    user_id = fields.Many2one('res.users',"Created by", required=True, default=lambda self: self.env.user, readonly=True)
    image_field = fields.Image(related = 'product_id.image_1920')
    image = fields.Many2many('ir.attachment', string="Image",required = True)
    notes = fields.Text('Notes' ,required = True)
    product_expiry_alert = fields.Boolean(compute='_compute_product_expiry_alert',
                                          help="The Expiration Date has been reached.")
    state_warning = fields.Selection([
        ('unconfirm','Unconfimred'),
        ('confirm','Confirmed'),
        ('moved','Moved')],
        'State Warning',
        default='unconfirm')

    def to_confirm(self):
        self.state_warning = 'confirm'

    def to_move(self):
        self.state_warning = 'moved'

    def to_set_price(self):
        self.ensure_one()
        view = self.env.ref('product.product_pricelist_view')
        return {
            'name': _('ListPrice'),
            'view_mode': 'form',
            'res_model': 'product.pricelist',
            'view_id': view.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def to_scrap(self):
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

    def to_return(self):
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


    @api.depends('expiration_date')
    def count_time_left(self):
        if self.expiration_date is not False:
            current_time = datetime.now().day
            if self.expiration_date.day > current_time:
                self.time_left = (self.expiration_date.day - current_time)
            else:
                self.time_left = -(current_time - self.expiration_date.day)

    # @api.depends('expiration_date')
    # def _compute_product_expiry_alert(self):
    #     current_date = fields.Datetime.now()
    #     for lot in self:
    #         if lot.expiration_date:
    #             lot.product_expiry_alert = lot.expiration_date <= current_date
    #         else:
    #             lot.product_expiry_alert = False












