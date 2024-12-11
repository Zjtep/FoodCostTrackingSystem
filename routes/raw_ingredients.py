from flask import Blueprint, request, jsonify
from extensions import db
from models.raw_ingredient import RawIngredient

# Create the blueprint
raw_ingredients_blueprint = Blueprint('raw_ingredients', __name__)

# Define the routes
@raw_ingredients_blueprint.route('/add_raw', methods=['POST'])
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

@raw_ingredients_blueprint.route('/get_raw', methods=['GET'])
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
