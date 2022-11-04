import re
from flask import Blueprint, jsonify, request, make_response,abort
from app.models.planet import Planet
from app import db

'''
class Planet:
    def __init__(self, id, name, description, color):
        self.id = id
        self.name = name
        self.description = description
        self.color = color

planets = [
    Planet(1, "Mercury", "smallest planet", "tan"), 
    Planet(2, "Venus", "hottest planet", "tan"), 
    Planet(3, "Earth", "home planet", "blue"), 
    Planet(4, "Mars", "dusty and cold", "red")]
'''



planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")


@planets_bp.route('', methods = ["GET"])
def get_all_planets():
    name_query_value = request.args.get("name")
    if name_query_value is not None:
        planets = Planet.query.filter_by(name = name_query_value)
    else:
        planets = Planet.query.all()
        
    planet_response = []
    for planet in planets:     
        planet_response.append(planet.to_dict())   

    return jsonify(planet_response), 200
    
'''
@planets_bp.route("/<planet_id>", methods = ["GET"])
def get_single_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError: 
        return jsonify({"msg":f"invalid data type: {planet_id}"}), 400

    chosen_planet = None
    for planet in planets:
        if planet.id == planet_id:
            chosen_planet = planet

            return_planet = {
                "id": chosen_planet.id,
                "name": chosen_planet.name,
                "description": chosen_planet.description,
                "color": chosen_planet.color
            }
            return jsonify(return_planet), 200
    if planet_id not in planets:
        return jsonify({"msg": f"can't find planet id {planet_id}"}), 404
    
'''   

@planets_bp.route("", methods=['POST'])
def create_a_planet():
    request_body = request.get_json()  #we are signaling to flask to look for anything with json object
    
    # new_planet = Planet(name=request_body['name'],
    #                     description=request_body['description'],
    #                     color=request_body['color'])
    
    new_planet=Planet.from_dict(request_body)
    
    db.session.add(new_planet)
    db.session.commit()
    
    return make_response(f"Planet {new_planet.name} successfully created", 201)


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    chosen_planet = validate_model_id(Planet, planet_id)
    return jsonify(chosen_planet.to_dict()), 200
    
@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_one_planet(planet_id):
    update_planet = validate_model_id(Planet, planet_id)
    request_body = request.get_json()
    planet_attributes = ["name", "description", "color"]
    response = ""
    
    try:
        update_planet.name = request_body["name"]
        update_planet.description = request_body["description"]
        update_planet.color = request_body["color"]
    except KeyError:
        for attribute in planet_attributes:
            if attribute not in request_body:
                response += attribute + ", "
        return jsonify({"message": f"Planet #{planet_id} missing {response[:-2]}"}), 200

    # try:
    #     update_planet.name = request_body["name"]
    # except KeyError:
    #     return jsonify({"message":"missing name information"}), 400
    # try:
    #     update_planet.description = request_body["description"]
    # except KeyError:
    #     return jsonify({"message":"missing planet description information"}), 400
    # try:
    #     update_planet.color = request_body["color"]
    # except KeyError:
    #     return jsonify({"message":"missing planet color information"}), 400
    
    db.session.commit()
    
    return jsonify({"message":f"Planet {update_planet.name} id#{planet_id} successfully updated"}), 200
    
    
@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    
    planet_to_delete = validate_model_id(Planet,planet_id)
    
    db.session.delete(planet_to_delete)
    db.session.commit()
    
    return jsonify({"message":f"Planet {planet_to_delete.name} id #{planet_id} successfully deleted"}),200


def validate_model_id(cls,model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message":f"{cls.__name__} id {model_id} is invalid"},400))
    
    chosen_object = cls.query.get(model_id)
    
    if chosen_object is None:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
        
    return chosen_object