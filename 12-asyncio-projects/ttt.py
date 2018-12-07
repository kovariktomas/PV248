import asyncio
import sys
import urllib
import os
from socketserver import ThreadingMixIn
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler
import socketserver
import re
import json
import shutil
from random import randint


def new_game(self, dict):

    try:
        request_path = urllib.parse.urlparse(self.path).path
        params = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(params)

        id = randint(1, 1000000)
        while id in dict:
            id = randint(1, 1000000)

        game_dict = {}
        game_dict["name"] = params["name"][0]

        board = []
        board.append([0, 0, 0])
        board.append([0, 0, 0])
        board.append([0, 0, 0])

        game_dict["board"] = board
        game_dict["next"] = 1
        game_dict["winner"] = -1

        dict[id] = game_dict

        dataForJson = {}
        dataForJson["id"] = id
        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)
    except:
        dataForJson = {}
        dataForJson["bad"] = "Nespravne parametry!"
        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)


def status_game(self, dict):

    try:
        request_path = urllib.parse.urlparse(self.path).path
        params = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(params)

        #print (request_path)
        #print (params)

        try:
            game_id = int(params["game"][0])
            game = dict[game_id]
        except:
            self.send_error(404, 'Game not found')
            return

        dataForJson = {}

        if game["winner"] != -1:
            dataForJson["board"] = game["board"]
            dataForJson["winner"] = game["winner"]
        else:
            dataForJson["board"] = game["board"]
            dataForJson["next"] = game["next"]

        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)
    except:
        dataForJson = {}
        dataForJson["bad"] = "Nespravne parametry!"
        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)


def play_game(self, dict):

    try:
        request_path = urllib.parse.urlparse(self.path).path
        params = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(params)

        #print (request_path)
        #print (params)

        try:
            game_id = int(params["game"][0])
            game = dict[game_id]
        except:
            self.send_error(404, 'Game not found')
            return

        game_id = int(params["game"][0])
        player = int(params["player"][0])
        x = int(params["x"][0])
        y = int(params["y"][0])

        dataForJson = {}

        if not (dict[game_id]["winner"] == -1):
            dataForJson["message"] = "Hra jiz skoncila, nelze dale hrat!"
            dataForJson["status"] = "bad"
        elif not (player == dict[game_id]["next"]):
            dataForJson["message"] = "Hrac " + str(player) + " neni na rade!"
            dataForJson["status"] = "bad"
        elif (x < 0 or x > 2 or y < 0 or y > 2):
            dataForJson["message"] = "Mimo rozsah hraciho pole!"
            dataForJson["status"] = "bad"
        elif not (dict[game_id]["board"][x][y] == 0):
            dataForJson["message"] = "Pole je jiz obsazeno!"
            dataForJson["status"] = "bad"
        else:
            dict[game_id]["board"][x][y] = player
            game_ower(dict, game_id)
            dataForJson["status"] = "ok"

            if player == 1:
                dict[game_id]["next"] = 2
            elif player == 2:
                dict[game_id]["next"] = 1


        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)
    except:
        dataForJson = {}
        dataForJson["bad"] = "Nespravne parametry!"
        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)


def play_list(self, dict):

    try:
        request_path = urllib.parse.urlparse(self.path).path
        params = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(params)

        dataForJson = []

        for id, game in dict.items():
            game_dict = {}
            game_dict["id"] = id
            game_dict["name"] = game["name"]
            dataForJson.append(game_dict)

        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)
    except:
        dataForJson = {}
        dataForJson["bad"] = "Nespravne parametry!"
        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)


def  game_ower(dict, game_id):

    game = dict[game_id]

    board = dict[game_id]["board"]

    cnt_zeros = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                cnt_zeros += 1

    if cnt_zeros == 0:
        dict[game_id]["winner"] = 0

    players = [1, 2]

    for p in players:
        for i in range(3):
            if board[i][0] == p and board[i][1] == p and board[i][2] == p:
                dict[game_id]["winner"] = p
            if board[0][i] == p and board[1][i] == p and board[2][i] == p:
                dict[game_id]["winner"] = p

        if board[0][0] == p and board[1][1] == p and board[2][2] == p:
            dict[game_id]["winner"] = p
        if board[2][0] == p and board[1][1] == p and board[0][2] == p:
            dict[game_id]["winner"] = p




def create_handler():

    dict = {}

    class Handler(CGIHTTPRequestHandler):

        def do_GET(self):
            params = str(self.path).split("?", 1)[-1]
            request_path = urllib.parse.urlparse(self.path).path

            if(request_path == "/start" or request_path == "/start/"):
                new_game(self, dict)
            elif (request_path == "/status" or request_path == "/status/"):
                status_game(self, dict)
            elif (request_path == "/play" or request_path == "/play/"):
                play_game(self, dict)
            elif (request_path == "/list" or request_path == "/list/"):
                play_list(self, dict)
            else:
                dataForJson = {}
                dataForJson["bad"] = "Nespravny dotaz!"
                json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
                json_string = bytes(json_string, 'utf-8')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json_string)




    return Handler

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    port = int(sys.argv[1])

    h = create_handler()

    server = ThreadedHTTPServer(('127.0.0.1', int(sys.argv[1])), h)

    print ('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

main()



