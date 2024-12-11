
from extensions import db

class InHouseIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)
    total_measurement = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    @property
    def price_per_unit(self):
        return self.total_cost / self.total_measurement if self.total_measurement else 0

class InHouseComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    in_house_id = db.Column(db.Integer, db.ForeignKey('in_house_ingredient.id'), nullable=False)
    raw_id = db.Column(db.Integer, db.ForeignKey('raw_ingredient.id'), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)

    in_house = db.relationship('InHouseIngredient', backref=db.backref('components', lazy=True))
    raw = db.relationship('RawIngredient')
    