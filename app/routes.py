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
    planet_response = []
    planets = Planet.query.all()

    for planet in planets:        
        planet_response.append({
            "id": planet.id, 
            "name": planet.name, 
            "description": planet.description, 
            "color": planet.color})

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
    
    new_planet = Planet(name=request_body['name'],
                        description=request_body['description'],
                        color=request_body['color'])
    
    db.session.add(new_planet)
    db.session.commit()
    
    return make_response(f"Planet {new_planet.name} successfully created", 201)


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    chosen_planet = validate_planet(planet_id)
    return jsonify(chosen_planet.to_dict()), 200
    
    

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({"message":f"Planet id {planet_id} is invalid"},400))
    
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        abort(make_response({"message":f"Planet {planet_id} not found"}, 404))
        
    return planet