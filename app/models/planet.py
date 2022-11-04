from app import db 

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =db.Column(db.String)
    description=db.Column(db.String)
    color=db.Column(db.String)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color
        }
        
    @classmethod
    def from_dict(cls, planet_dict):
        return cls(
            name=planet_dict["name"],
            description=planet_dict["description"],
            color=planet_dict["color"]
        )
        