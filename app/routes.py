from flask import Blueprint, jsonify

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

planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")
@planets_bp.route('', methods = ["GET"])

def get_all_planets():
    planet_dicts = []

    for planet in planets:
        dict = {
            "id": planet.id, 
            "name": planet.name, 
            "description": planet.description, 
            "color": planet.color}

        planet_dicts.append(dict)

    return jsonify(planet_dicts), 200