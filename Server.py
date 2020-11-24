import sys
import json
import datetime
import time
import random
import socket
from _thread import *
from operator import itemgetter
import pickle
import requests

HOST = ''
PORT = 12345


def MatchMakingRoom(sock):
    while True:
        sock.listen()
        conn, addr = sock.accept()

        with conn:
            playerID: conn.recv(1024)
            playerID = pickle.loads(playerID)
            print('Recieved', playerID)

            if playerID != "":
                response = requests.get('https://17wlo7p4ed.execute-api.us-east-1.amazonaws.com/default/A3-Lambda')
            
                players = response.json()['Items']

                ratio = 20
                requestMatches = None

                for player in players:
                    if player['user_id'] == playerID:
                        playerRequestFound = player
                    if player['matches'] < 3:
                        player['ratio'] = 50

                playersLookingForMatch = []

                for player in players:
                    if abs(player['ratio'] - playerRequestFound['ratio']) < ratio and player != playerRequestFound:
                        playersLookingForMatch.append(player)

                PlayerRatioTable = sorted(playersLookingForMatch, key=itemgetter('ratio'))

                playersDictonary = [
                    (player, abs(player['ratio'] - playerRequestFound['ratio'])) for player in PlayerRatioTable
                ]

                playersDictonary.sort(key=itemgetter(1))

                finalLeaderboard = [seq[0] for seq in playersDictonary]

                while len(finalLeaderboard) > 2:
                    finalLeaderboard.pop()

                finalLeaderboard.append(playerRequestFound)

                response = pickle.dumps(finalLeaderboard)
                conn.sendall(response)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    start_new_thread(MatchMakingRoom, (s,))

    while True:
        time.sleep(1)
        print("Waiting for Players...")