from odoo import fields, models, api, exceptions

class TravelMgmt(models.Model):
    _name = "travel.mgmt"
    _description = "Travel Management"

    # Rappresenta il nome della spesa
    name = fields.Char(string="Name")

    # Rappresenta La data di inizio del viaggio
    date_start = fields.Date(string="Date From")

    # Rappresenta La data di fine del viaggio
    date_end = fields.Date(string="Date To")

    # Il dipendente che ha fatto il viaggio. Prende di default il dipendente collegato all’utente corrente
    employee_id = fields.Many2one("hr.employee",
        string="Employee",
        default=lambda self: self.env.user,
    )

    # L’azienda del dipendente. Prende di default verso l’azienda corrente
    company_id = fields.Many2one('res.company',
        string="Companies",
        default=lambda self: self.env.company,
    )

    # Campo note generico.
    notes = fields.Text(string="Note")

    # Da chi verrà pagata la spesa
    # Servirà nella creazione della nota spese per valorizzare l’omonimo campo
    payed_by = fields.Selection(
        string='Payed By',
        selection=[
            ('own_account', 'Employee'),
            ('company_account', 'Company'),
            ],
    )

    # Identifica lo stato con due valori: Bozza (default) e Spese Create.
    state = fields.Selection(
        selection=[
            ('draft','Draft'),
            ('request','Expense Request')
        ],
        default='draft'
    )

    # Campo relazionale che rappresenta le spese
    travel_mgmt_lines_ids = fields.One2many('travel.mgmt.line','travel_id',string="Expenses")
    

    # -------------------------------------------------------------------------
    # CONSTRAINS METHODS
    # -------------------------------------------------------------------------

    @api.constrains('date_start','date_end')
    def _date_end_constraint(self):
        for record in self:
            if record.date_start > record.date_end:
                raise exceptions.ValidationError("Data Da deve Essere minore di Data A")
    
    # -------------------------------------------------------------------------
    # ACTION METHODS
    # -------------------------------------------------------------------------

    def action_create_expense(self):
        for record in self:
            
            for line in record.travel_mgmt_lines_ids:

                if not record.name:
                    raise exceptions.ValidationError("Travel name is necessary")

                expense = self.env['hr.expense'].create({
                    'name': record.name,
                    'employee_id': record.employee_id.id,
                    'company_id': record.company_id.id,
                    'payment_mode': record.payed_by,
                    'date': line.date,
                    'price_unit': line.unit_price,
                    'quantity': line.quantity,
                    'product_id': line.product_id.id,
                })

            record.state = 'request'

        return True