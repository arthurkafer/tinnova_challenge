from flask import Flask, request, jsonify
from cars_app import CarsApp, InvalidUsage

api = Flask(__name__)
app = CarsApp()

@api.errorhandler(InvalidUsage)
def error_handle(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@api.route("/veiculos", methods=["GET"]) 
def get_vehicles():
	params = request.args
	if not params:
		return app.get_all_vehicles()
	else:
		return app.get_vehicles(params)
	
@api.route('/veiculos/<int:id>', methods=['GET'])
def get_vehicle_by_id(id):
    return app.get_vehicles({"id":id})

@api.route('/veiculos', methods=['POST'])
def add_vehicle():
	data = request.get_json()
	return app.add_vehicle(data) # 201

@api.route('/veiculos/<int:id>', methods=['PUT'])
def update_complete_vehicle(id):
	data = request.get_json()
	return app.update_vehicle(data, id)

@api.route('/veiculos/<int:id>', methods=['PATCH'])
def update_vehicle(id):
    data = request.get_json()
    return app.update_vehicle(data, id)

@api.route('/veiculos/<int:id>', methods=['DELETE'])
def delete_veiculo(id):
    return app.delete_vehicle(id)

if __name__ == "__main__":
	api.run(host="0.0.0.0", port=8081)