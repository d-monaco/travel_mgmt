from odoo import fields, models, api, exceptions

class TravelMgmtLine(models.Model):
    _name = "travel.mgmt.line"
    _description = "Travel Management Line"

    # Prodotto: Relazionale verso i prodotti.
    # Sul prodotto aggiungere un domain che faccia prendere solo i
    # prodotti che hanno a true il campo can_be_expensed (introdotto dal modulo hr_expense)
    product_id = fields.Many2one('product.product',
        domain=[('can_be_expensed', '=', True)],
    )

    # Decimale che rappresenta la quantità
    quantity = fields.Float()

    # Decimale che rappresenta il prezzo unitario. Di default il prezzo del prodotto
    unit_price = fields.Float(compute='_compute_unit_price')

    # Data della spesa.
    date = fields.Date()

    # Il viaggio a cui le spese sono legate
    travel_id = fields.Many2one('travel.mgmt', required=True)


    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends("product_id")
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.product_id.standard_price


    # -------------------------------------------------------------------------
    # CONSTRAINS METHODS
    # -------------------------------------------------------------------------

    @api.constrains('date')
    def _date_constraint(self):
        for record in self:
            if record.travel_id.date_end and record.travel_id.date_start:
                if record.date > record.travel_id.date_end or record.date < record.travel_id.date_start:
                    raise exceptions.ValidationError("The expense date must be within the travel period")
    