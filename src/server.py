from flask import Flask, request, jsonify, render_template
from cars_app import CarsApp, InvalidUsage
from datetime import datetime, timedelta

api = Flask(__name__, template_folder='../templates', static_folder="../static")
app = CarsApp()

@api.errorhandler(InvalidUsage)
def error_handle(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@api.route("/", methods=["GET"])
def index():
	filter_vehicle_name = request.args.get('veiculo', '')
	filter_brand = request.args.get('marca', '')
	filter_year = request.args.get('ano', '')

	filters_dict = {}
	if filter_vehicle_name: filters_dict['veiculo'] = filter_vehicle_name
	if filter_brand: filters_dict['marca'] = filter_brand
	if filter_year: filters_dict['ano'] = filter_year

	vehicles = app.get_all_vehicles() if not filters_dict else app.get_vehicles(filters_dict)

	# Calculate statistics
	unsold_vehicles_count = sum(1 for v in vehicles if not v['vendido'])

	vehicles_by_decade = {}
	for v in vehicles:
		if v['ano']:
			decade = (v['ano'] // 10) * 10
			vehicles_by_decade[decade] = vehicles_by_decade.get(decade, 0) + 1

	vehicles_by_brand = {}
	for v in vehicles:
		if v['marca']:
			vehicles_by_brand[v['marca']] = vehicles_by_brand.get(v['marca'], 0) + 1
			
	one_week_ago = datetime.now() - timedelta(days=7)
	vehicles_registered_last_week = [
		v for v in vehicles if datetime.strptime(v['created'], "%Y-%m-%dT%H:%M:%S") >= one_week_ago
	]
	return render_template('index.html', 
		vehicles=vehicles,
		unsold_vehicles_count=unsold_vehicles_count,
		total_vehicles_count=len(vehicles),
		unique_brands_count=len(vehicles_by_brand),
		vehicles_registered_last_week_count=len(vehicles_registered_last_week),
		vehicles_registered_last_week=vehicles_registered_last_week,
		filters=filters_dict,
		editing_vehicle=None # For add form initially
	)

@api.route('/api/chart_data')
def chart_data_api():
    vehicles = app.get_all_vehicles()
    
    vehicles_by_decade = {}
    for v in vehicles:
        if v['ano']:
            decade = (v['ano'] // 10) * 10
            vehicles_by_decade[decade] = vehicles_by_decade.get(decade, 0) + 1

    sorted_decades = sorted(vehicles_by_decade.items())
    
    vehicles_by_brand = {}
    for v in vehicles:
        if v['marca']:
            vehicles_by_brand[v['marca']] = vehicles_by_brand.get(v['marca'], 0) + 1

    sorted_brands = sorted(vehicles_by_brand.items(), key=lambda item: item[1], reverse=True)

    return jsonify({
        'decades': [{'name': f"{d[0]}s", 'count': d[1]} for d in sorted_decades],
        'brands': [{'name': b[0], 'count': b[1]} for b in sorted_brands]
    })

@api.route('/edit/<string:id>', methods=['GET'])
def edit_vehicle_page(id):
    vehicle = app.get_vehicles({"id": id})
    if not vehicle:
        raise InvalidUsage("Veiculo nao encontrado", 404)

    return render_template("edit_vehicle.html", vehicle=vehicle)

@api.route("/veiculos", methods=["GET"]) 
def get_vehicles():
	params = request.args
	if not params:
		return app.get_all_vehicles()
	else:
		return app.get_vehicles(params)
	
@api.route('/veiculos/<string:id>', methods=['GET'])
def get_vehicle_by_id(id):
    return app.get_vehicles({"id":id})

@api.route('/veiculos', methods=['POST'])
def add_vehicle():
	data = request.get_json()
	return app.add_vehicle(data) # 201

@api.route('/veiculos/<string:id>', methods=['PUT'])
def update_complete_vehicle(id):
	data = request.get_json()
	app.check_complete_payload(data)
	return app.update_vehicle(data, id)

@api.route('/veiculos/<string:id>', methods=['PATCH'])
def update_vehicle(id):
    data = request.get_json()
    return app.update_vehicle(data, id)

@api.route('/veiculos/<string:id>', methods=['DELETE'])
def delete_veiculo(id):
    return app.delete_vehicle(id)

if __name__ == "__main__":
	api.run(host="0.0.0.0", port=8081)