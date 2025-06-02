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
            {"id": uuid4().hex, "veiculo":"Chevette", "marca": "Chevrolet", "ano": 1982, "descricao": "Carro compacto", "vendido": False, "cor": "preto", "created": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S"), "updated": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")},
            {"id": uuid4().hex, "veiculo":"Opala", "marca": "Chevrolet", "ano": 1988, "descricao": "Carro de luxo", "vendido": True, "cor": "cinza", "created": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S"), "updated": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")},
            {"id": uuid4().hex, "veiculo":"Polo", "marca": "Volkswagen", "ano": 2019, "descricao": "Carro compacto", "vendido": False, "cor": "cinza", "created": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S"), "updated": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")},
            {"id": uuid4().hex, "veiculo":"Civic SI", "marca": "Honda", "ano": 2006, "descricao": "Carro esportivo", "vendido": True, "cor": "prata", "created": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S"), "updated": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")},
            {"id": uuid4().hex, "veiculo":"Gol GTS", "marca": "Volkswagen", "ano": 1994, "descricao": "Carro esportivo antigo", "vendido": True, "cor": "preto", "created": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S"), "updated": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")},
        ]
    
    def indexof_key_in_list(self, lista, key, value):
        return next((index for (index, d) in enumerate(lista) if d[key] == value), None)
    
    def check_complete_payload(self, payload):
        fields = ['marca', 'veiculo', 'ano', 'cor', 'vendido', 'descricao']
        for field in fields:
            if field not in payload:
                raise InvalidUsage("Campo obrigatorio nao informado", 422)
        if not type(payload["ano"]) is int and type(payload["vendido"]) is bool:
            raise InvalidUsage("Campo com formatacao incorreta", 422)
        return True

    def get_all_vehicles(self):
        return self.database
    
    def get_vehicles(self, query={}):
        filtered = self.database.copy()
        if "id" in query:
            vehicle = next((v for v in filtered if v["id"] == query["id"]), {})
            return vehicle
        
        if "marca" in query:
            filtered = [v for v in filtered if v["marca"] == query["marca"]]
        if "ano" in query:
            try:
                ano = int(query['ano'])
                filtered = [v for v in filtered if v["ano"] == ano]
            except ValueError:
                raise InvalidUsage("Ano deve ser um valor inteiro", 422)
        if 'cor' in query:
            filtered = [v for v in filtered if v["cor"].lower() == query['cor'].lower()]

        return filtered
    
    def add_vehicle(self, vehicle_data):
        self.check_complete_payload(vehicle_data)
        if vehicle_data["marca"] not in self.usable_brands:
            raise InvalidUsage("Marca nao existe no banco de dados", 422)

        new_vehicle = {
            "id": uuid4().hex, 
            "veiculo": str(vehicle_data["veiculo"]),
            "marca": str(vehicle_data["marca"]), 
            "ano": int(vehicle_data["ano"]), 
            "descricao": str(vehicle_data["descricao"]), 
            "vendido": bool(vehicle_data["vendido"]), 
            "cor": vehicle_data["cor"], 
            "created": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S"), 
            "updated": datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")
        }
        self.database.append(new_vehicle)
        return new_vehicle
    
    def update_vehicle(self, vehicle_data, id):
        vehicle = self.get_vehicles({"id": id})
        if not vehicle:
            raise InvalidUsage("Veiculo nao encontrado", 404)
        
        if "marca" in vehicle_data and vehicle_data["marca"] not in self.usable_brands:
            raise InvalidUsage("Marca nao existe no banco de dados", 422)
        
        updated_vehicle = vehicle.copy()
        updated_vehicle["updated"] = datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")
        for item in vehicle_data:
            updated_vehicle[item] = vehicle_data[item]
        return updated_vehicle
    
    def delete_vehicle(self, id):
        vehicle = self.get_vehicles({"id": id})
        if not vehicle:
            raise InvalidUsage("Veiculo nao encontrado", 404)
        
        idx = self.indexof_key_in_list(self.database, "id", id)
        del self.database[idx]
        return vehicle