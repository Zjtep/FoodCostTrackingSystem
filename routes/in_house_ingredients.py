
from flask import Blueprint, request, jsonify
from extensions import db
from models.in_house_ingredient import InHouseIngredient, InHouseComponent
from models.raw_ingredient import RawIngredient

in_house_ingredients_blueprint = Blueprint('in_house_ingredients', __name__)

@in_house_ingredients_blueprint.route('/add_in_house', methods=['POST'])
def add_in_house():
    data = request.json
    total_cost = 0
    total_measurement = 0
    in_house = InHouseIngredient(
        name=data['name'],
        unit_of_measure=data['unit_of_measure'],
        total_measurement=0,
        total_cost=0
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

@in_house_ingredients_blueprint.route('/get_in_house', methods=['GET'])
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
    