from flask import Blueprint, jsonify, request, abort, make_response
from app.models.humans import Human
from app.models.cats import Cat
from app import db

humans_bp = Blueprint('humans_bp', __name__, url_prefix='/humans')

def validate_human(human_id):
    try:
        human_id = int(human_id)
    except:
        abort(make_response({'msg': 'Invalid human id'}, 400))

    human = Human.query.get(human_id)
    if not human:
        abort(make_response({'msg': 'There is no human with that id'}, 404))    
    
    return human

@humans_bp.route('', methods=['POST'])
def create_human():
    request_body = request.get_json()

    try:
        new_human = Human(name=request_body['name'])
    except:
        return jsonify({'msg': 'Name is required'}), 404
    
    db.session.add(new_human)
    db.session.commit()

    return jsonify({'msg': f'Human with id {new_human.id} was created'}), 201

@humans_bp.route('', methods=['GET'])
def get_all_humans():
    humans = Human.query.all()
    
    humans_response = []
    for human in humans:
        humans_response.append({
            'name': human.name,
            'id': human.id})
    
    return jsonify(humans_response), 200

@humans_bp.route('/<human_id>/cats', methods=['POST'])
def create_cat(human_id):
    human = validate_human(human_id)

    request_body = request.get_json()

    try:
        new_cat = Cat(
                name=request_body['name'],
                color=request_body['color'],
                age=request_body['age'],
                human=human
        )
    except KeyError:
        return jsonify({'msg': 'Name, color and age are required'}), 404

    db.session.add(new_cat)
    db.session.commit()

    return jsonify({'msg': f'New cat with id {new_cat.id} was created'}), 201

@humans_bp.route('/<human_id>/cats', methods=['GET'])
def get_cats(human_id):
    human = validate_human(human_id)

    all_cats = []
    for cat in human.cats:
        all_cats.append({
            'id': cat.id,
            'name': cat.name,
            'color': cat.color,
            'age': cat.age
        })
    
    return jsonify(all_cats), 200
