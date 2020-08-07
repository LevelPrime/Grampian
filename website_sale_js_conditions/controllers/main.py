# Copyright 2020 Level Prime limited - Roberto Fichera
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID
from odoo.http import request
from odoo.addons.website_sale.controllers import main


class WebsiteSale(main.WebsiteSale):
    def _get_mandatory_billing_fields(self):
        result = super(WebsiteSale, self)._get_mandatory_billing_fields()
        return result + self._mandatory_legal_terms()

    def _get_mandatory_shipping_fields(self):
        result = super(WebsiteSale, self)._get_mandatory_shipping_fields()
        return result + self._mandatory_legal_terms()

    def _mandatory_legal_terms(self):
        """Require ``accepted_legal_terms`` only if we are validating."""
        result = []
        if request.context.get("needs_legal"):
            result.append("accepted_legal_terms")
            result.append("accepted_data_terms")
        return result

    def checkout_form_validate(self, mode, all_form_values, data):
        """Require accepting legal terms to validate form."""
        # Patch context
        old_context = request.context
        new_context = dict(request.context, needs_legal=True)
        request.context = new_context
        result = super(WebsiteSale, self).checkout_form_validate(
            mode, all_form_values, data)
        # Unpatch context
        request.context = old_context
        return result

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSale, self)._checkout_form_save(
            mode, checkout, all_values)
        accepted_legal_terms = all_values.get('accepted_legal_terms')
        accepted_data_terms =  all_values.get('accepted_data_terms')
        accepted_marketing_terms = all_values.get('accepted_marketing_terms')
        if (all_values.get('submitted') and accepted_legal_terms and accepted_data_terms):
            environ = request.httprequest.headers.environ
            metadata = "Website legal terms acceptance metadata:<br/>"
            metadata += "Agreed T&C: {}<br/>".format('Yes' if accepted_legal_terms else 'No')
            metadata += "Agreed Data Handling: {}<br/>".format('Yes' if accepted_data_terms else 'No')
            metadata += "Agreed Marketing Usage: {}<br/>".format('Yes' if accepted_marketing_terms else 'No')
            metadata += "<br/>".join(
                "%s: %s" % (val, environ.get(val)) for val in (
                        "REMOTE_ADDR",
                        "HTTP_USER_AGENT",
                        "HTTP_ACCEPT_LANGUAGE",
                    )
                )
            partner_id = request.env['res.partner'].browse(res)
            partner_id.sudo().write({'optin_marketing': accepted_marketing_terms})
            website_user = request.website.salesperson_id.id or SUPERUSER_ID
            partner_id.sudo(website_user).message_post(
                body=metadata, message_type='notification')
        return res
