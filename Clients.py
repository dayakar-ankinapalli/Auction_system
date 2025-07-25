from flask import Flask
import json, bcrypt


app = Flask(__name__)

class Client:
    def __init__(self):
        self.clients = {}
        self.current_port = 8001  # Starting port number

    def register(self, username, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        #Create an initial JSON file if it doesn't exist with an empty list of clients
        with open('clients.json', 'r') as file:
            clients_data = json.load(file)

        for client in clients_data['clients']:
            if client['email'] == email:
                return {'message': 'Email already registered. Please use a different email.'}
            if not email.endswith('@gmail.com'):
                return {'message':'Invalid email format'}

        new_client = {
            'username': username,
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'port': self.current_port
        }
        self.current_port += 1  # Increment the port number

        clients_data['clients'].append(new_client)

        with open('clients.json', 'w') as file:
            json.dump(clients_data, file, indent=4)

        return {'message': 'Registration successful.', 'port': new_client['port']}

    def validate_login(self, email, password):
        with open('clients.json', 'r') as file:
            clients_data = json.load(file)

        for client in clients_data['clients']:
            if client['email'] == email:
                # Validate the password
                if bcrypt.checkpw(password.encode('utf-8'), client['password'].encode('utf-8')):
                    return {'message': 'Login successful.', 'port': client['port']}
                else:
                    return {'message': 'Invalid password.'}

        return {'message': 'Email not found.'}


if __name__ == '__main__':
    client = Client()
    app.run(port=client.current_port)