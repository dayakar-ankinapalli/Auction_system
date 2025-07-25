from flask import Flask, request, jsonify

app = Flask(__name__)

from Clients import Client
from Auctioneer import Auctioneer

client = Client()
auctioneer = Auctioneer()

@app.route('/registration', methods=['POST'])
def registration():
    data = request.get_json()

    username = data['username']
    email = data['email']
    password = data['password']

    response = client.register(username, email, password)
    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    response = client.validate_login(email, password)
    return jsonify(response)

@app.route('/slot1_bid/<int:port>', methods=['POST'])
def slot1_bid(port):
    data = request.get_json()

    email = data['email']
    slots = int(data['slots'])
    bid_price = int(data['bid_price'])

    response = auctioneer.submit_bid(email, slots, bid_price, port)

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9001)