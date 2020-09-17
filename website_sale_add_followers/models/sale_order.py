from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'sale':
            for record in self:
                if record.website_id.id and record.website_id.salesteam_id.id and \
                        record.website_id.salesteam_id.member_ids.ids:
                    record.message_subscribe(record.website_id.salesteam_id.member_ids.partner_id.ids)

        res = super(SaleOrder, self).write(vals)
        return res
