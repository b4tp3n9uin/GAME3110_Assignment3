import json
import socket
import random
import logging
import requests
import time
import ast
import pickle

HOST = 'localhost'
PORT = 12345

def simulation():
    IDlist = ['matthew', 'cristhian', 'nini', 'skiup', 'shannon', 'prem', 'mahedi', 'nic', 'laurence', 'teddy']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        id = pickle.dumps(random.choice(IDlist))
        print('Send ', id)
        s.sendall(id)
        data = s.recv(1024)

    playersIngame = pickle.loads(data)

    matches = []

    if len(playersIngame) == 3:
        for player in playersIngame:
            matches.append(player['user_id'])

        print("Match Closed!")
        logging.info("Match Closed!")

        for player in matches:
            logging.info('Player: '+player+ ' connected')

        for player in playersIngame:
            print('Player ' +player['user_id']+ 'level: ' +str(player['ratio']))

        winner = random.choice(matches)
        matches.remove(winner)

        requests.get('https://wehnu0siod.execute-api.us-east-1.amazonaws.com/default/updatePlayers', params={'user_id': winner, 'win': 'true'})

        response = requests.get('https://17wlo7p4ed.execute-api.us-east-1.amazonaws.com/default/A3-Lambda')

        print('Winner: ' +winner)
        logging.info('Winner: ' +winner)

        players = response.json()['Items']

        for player in players:
            if player['user_id'] == str(winner):
                print(player['user_id'] + ', level: ' + str(player['ratio']))
                logging.info(player['user_id'] + ', level: ' + str(player['ratio']))

        for loser in matches:
            requests.get('https://wehnu0siod.execute-api.us-east-1.amazonaws.com/default/updatePlayers', params={'user_id': loser, 'win': 'true'})
            response = requests.get('https://17wlo7p4ed.execute-api.us-east-1.amazonaws.com/default/A3-Lambda')

            players = response.json()['Items']
            for player in players:
                if player['user_id'] == loser:
                    print(player['user_id'] + ' current level: ' + str(player['ratio']))
                    logging.info(player['user_id'] + ' current level: ' + str(player['ratio']))

    else:
        print('No Match Found!')
        logging.info('No Match Found!')

if __name__ == '__main__':
    RoundsNumber = input("Enter the amount of matches to simulate: ")

    for i in range(int(RoundsNumber)):
        simulation()
