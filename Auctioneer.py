import json
import random

class Auctioneer:
    def submit_bid(self, email, slots, bid_price, port):
        with open('clients.json', 'r') as file:
            clients_data = json.load(file)

        # Find the client with the provided email
        client_found = False
        for client in clients_data['clients']:
            if client['email'] == email:
                client_found = True
                stored_port = client['port']
                break

        if not client_found:
            return {'message': 'Email not found.'}

        if port != stored_port:
            return {'message': 'Invalid port number.'}

        if slots < 1 or slots > 100:
            return {'message': 'Dear client, you can bid slots between 1 to 100.'}

        _base_price = 10
        total_price = slots * _base_price
        if total_price > bid_price:
            return {'message': 'Please increase the bid price you are lower than the base price.'}

        bid_data = {
            'slots': slots,
            'bid_price': bid_price,
            'port': port
        }

        # Update bid or add a new bid
        self._update_bid_data(bid_data, port)

        # Generating probability of your bid
        probability = self._check_probability()
        probability_string = f"{probability}%"

        # Update probability or add a new probability
        self._update_probability(port, probability_string)

        return {'message': 'Bid submitted successfully'}

    def _check_probability(self):
        probability = random.randint(1, 100)
        return probability

    def _update_bid_data(self, bid_data, port):
        with open('slot1_bid_submission.json', 'r+') as file:
            data = json.load(file)
            if 'slot1_bid_submission' in data:
                for bid in data['slot1_bid_submission']:
                    if bid['port'] == port:
                        bid.update(bid_data)  # Update existing bid
                        break
                else:
                    data['slot1_bid_submission'].append(bid_data)  # Add new bid if no matching port is found
            else:
                data['slot1_bid_submission'] = [bid_data]
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def _update_probability(self, port, probability_string):
        with open('slot1_probability.json', 'r+') as file:
            data = json.load(file)
            if 'slot1_probability' in data:
                for probability_entry in data['slot1_probability']:
                    if probability_entry['port'] == port:
                        probability_entry['probability'] = probability_string  # Update existing probability
                        break
                else:
                    data['slot1_probability'].append({'port': port, 'probability': probability_string})  # Add new probability if no matching port is found
            else:
                data['slot1_probability'] = [{'port': port, 'probability': probability_string}]
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()