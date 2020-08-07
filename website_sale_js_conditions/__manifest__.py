# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Require accept terms, conditions to checkout",
    "summary": "Force the user to accept legal tems, condition to buy in the web shop",
    "version": "13.0.1.0.0",
    "category": "Website",
    "website": "https://levelprime.com",
    "author": "Level Prime Limited",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale",
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/website_sale.xml",
    ],
}
