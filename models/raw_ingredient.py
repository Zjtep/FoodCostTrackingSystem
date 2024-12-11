from extensions import db

class RawIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)
    measurement = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

    @property
    def price_per_unit(self):
        return self.purchase_price / self.measurement if self.measurement else 0
