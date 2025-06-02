from datetime import datetime
from uuid import uuid4

class InvalidUsage(Exception):
	status_code = 500

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv

class CarsApp():
    def __init__(self):
        self.usable_brands = [
            "Fiat",
            "Volkswagen",
            "Chevrolet",
            "Hyundai",
            "Ford",
            "BMW",
            "Audi",
            "Mercedes-Benz",
            "Renault",
            "Peugeot",
            "Dodge",
            "Jeep",
            "BYD",
            "Toyota",
            "Nissan",
            "Honda",
        ]
        # usando database dentro de uma lista pra nao precisar implementar um banco
        self.database = [
            {"id": uuid4().hex, "veiculo":"Chevette", "marca": "Chevrolet", "ano": 1982, "descricao": "Carro compacto", "vendido": False, "cor": "preto", "created": datetime.now(), "updated": datetime.now()},
            {"id": uuid4().hex, "veiculo":"Opala", "marca": "Chevrolet", "ano": 1988, "descricao": "CCarro de luxo", "vendido": True, "cor": "cinza", "created": datetime.now(), "updated": datetime.now()},
            {"id": uuid4().hex, "veiculo":"Polo", "marca": "Volkswagen", "ano": 2019, "descricao": "Carro compacto", "vendido": False, "cor": "cinza", "created": datetime.now(), "updated": datetime.now()},
            {"id": uuid4().hex, "veiculo":"Civic SI", "marca": "Honda", "ano": 2006, "descricao": "Carro esportivo", "vendido": True, "cor": "prata", "created": datetime.now(), "updated": datetime.now()},
            {"id": uuid4().hex, "veiculo":"Gol GTS", "marca": "Volkswagen", "ano": 1994, "descricao": "Carro esportivo antigo", "vendido": True, "cor": "preto", "created": datetime.now(), "updated": datetime.now()},
        ]
    
    def check_complete_payload(self, payload):
        fields = ['marca', 'veiculo', 'ano', 'cor', 'vendido', 'descricao']
        for field in fields:
            if field not in payload:
                raise InvalidUsage("Campo obrigatorio nao informado", 422)
        return True

    def get_all_vehicles(self):
        return self.database
    
    def get_vehicles(self, query={}):
        return self.database
    
    def add_vehicle(self, vehicle_data):
        self.check_complete_payload(vehicle_data)
        if vehicle_data["marca"] not in self.usable_brands:
            raise InvalidUsage("Marca nao existe no banco de dados", 422)
        return True
    
    def update_vehicle(self, vehicle_data, id):
        if "marca" in vehicle_data and vehicle_data["marca"] not in self.usable_brands:
            raise InvalidUsage("Marca nao existe no banco de dados", 422)
        return True
    
    def delete_vehicle(self, id):
        return True