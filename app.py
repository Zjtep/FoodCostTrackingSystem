from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_cost.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Raw Ingredient model
class RawIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)
    measurement = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

    @property
    def price_per_unit(self):
        return self.purchase_price / self.measurement if self.measurement else 0

# Define In-House Ingredient model
class InHouseIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)
    total_measurement = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    @property
    def price_per_unit(self):
        return self.total_cost / self.total_measurement if self.total_measurement else 0

# Define In-House Ingredient Component model
class InHouseComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    in_house_id = db.Column(db.Integer, db.ForeignKey('in_house_ingredient.id'), nullable=False)
    raw_id = db.Column(db.Integer, db.ForeignKey('raw_ingredient.id'), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)

    in_house = db.relationship('InHouseIngredient', backref=db.backref('components', lazy=True))
    raw = db.relationship('RawIngredient')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_raw', methods=['POST'])
def add_raw():
    data = request.json
    new_raw = RawIngredient(
        name=data['name'],
        unit_of_measure=data['unit_of_measure'],
        measurement=data['measurement'],
        purchase_price=data['purchase_price']
    )
    db.session.add(new_raw)
    db.session.commit()
    return jsonify({'message': 'Raw ingredient added successfully!'})

@app.route('/get_raw', methods=['GET'])
def get_raw():
    raws = RawIngredient.query.all()
    return jsonify([
        {
            'id': raw.id,
            'name': raw.name,
            'unit_of_measure': raw.unit_of_measure,
            'measurement': raw.measurement,
            'purchase_price': raw.purchase_price,
            'price_per_unit': round(raw.price_per_unit, 2)
        } for raw in raws
    ])

@app.route('/add_in_house', methods=['POST'])
def add_in_house():
    data = request.json
    total_cost = 0
    total_measurement = 0
    in_house = InHouseIngredient(
        name=data['name'],
        unit_of_measure=data['unit_of_measure'],
        total_measurement=0,  # Placeholder, will calculate later
        total_cost=0  # Placeholder, will calculate later
    )
    db.session.add(in_house)
    db.session.flush()

    for component in data['components']:
        raw = RawIngredient.query.get(component['raw_id'])
        if not raw:
            continue
        cost = raw.price_per_unit * component['quantity_used']
        total_cost += cost
        total_measurement += component['quantity_used']
        in_house_component = InHouseComponent(
            in_house_id=in_house.id,
            raw_id=raw.id,
            quantity_used=component['quantity_used']
        )
        db.session.add(in_house_component)

    in_house.total_cost = total_cost
    in_house.total_measurement = total_measurement
    db.session.commit()
    return jsonify({'message': 'In-house ingredient created successfully!'})

@app.route('/get_in_house', methods=['GET'])
def get_in_house():
    in_houses = InHouseIngredient.query.all()
    return jsonify([
        {
            'id': in_house.id,
            'name': in_house.name,
            'unit_of_measure': in_house.unit_of_measure,
            'total_measurement': in_house.total_measurement,
            'total_cost': in_house.total_cost,
            'price_per_unit': round(in_house.price_per_unit, 2),
            'components': [
                {
                    'raw_name': component.raw.name,
                    'quantity_used': component.quantity_used,
                    'unit_of_measure': component.raw.unit_of_measure,
                    'price_per_unit': round(component.raw.price_per_unit, 2),
                    'cost': round(component.raw.price_per_unit * component.quantity_used, 2)
                } for component in in_house.components
            ]
        } for in_house in in_houses
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
