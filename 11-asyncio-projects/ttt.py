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

        game_id = int(params["game"][0])

        game = dict[game_id]

        dataForJson = {}

        if game["winner"] != -1:
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
            else:
                pass




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



