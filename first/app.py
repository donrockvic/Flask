from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='template')

stores = [
    {
        'name': 'My Wonderful store',
        'items': [{
            'name': 'My item',
            'price':  15.00
        }]
    }
]


@app.route('/')
def home():
    return render_template('index.html', )


# POST - used to receive data
# GET - used to send data back only

# POST /store data: {name}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_data = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_data)
    return jsonify(new_data)


# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_items_in_store(name):
    requested_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': requested_data['name'],
                'price': requested_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


app.run(port=5000)
