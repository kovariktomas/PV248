import sys
import json
import http.client
import socket
import ssl
import aiohttp
import asyncio
from time import sleep

async def fetch(session, url):
    async with session.get(url) as response:
        assert response.status == 200
        return await response.text()

def empty_board(board):
    cnt_zeros = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                cnt_zeros += 1

    return cnt_zeros == 9


def print_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                print ("_", end="", sep="")
            if board[i][j] == 1:
                print ("x", end="", sep="")
            if board[i][j] == 2:
                print ("o", end="", sep="")
        print("")


async def list_games(json_data, session):
    if len(json_data) > 0:
        print ("Muzete se prihlasit do nasledujicich her:")
        print ("ID \t\t Name")
        for game in json_data:
            json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/status?game=" + str(game["id"]))
            json_data = json.loads(json_response)
            if "board" in json_data:
                if empty_board(json_data["board"]):
                    print ("{} \t\t {}".format(game["id"], game["name"]))
        print("Zadejte id hry, nebo zalozte novou hru napsanim \"new\": ", sep='', end='')
        game_id = input()
        return game_id
    else:
        print ("Zadne volne hry. Zalozte novou hru napsanim \"new\".")
        game_id = input()
        return game_id

async def waiting(session, game_id, player):
    print_waiting = True
    print_board1 = True

    while True:
        json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/status?game=" + str(game_id))
        json_data = json.loads(json_response)

        if "next" in json_data:
            if print_board1 == True:
                print_board(json_data["board"])
                print_board1 = False
            if int(json_data["next"]) == player:
                print_board(json_data["board"])
                await play(session, game_id, player)

        elif "winner" in json_data:
            if int(json_data["winner"]) == player:
                print("you win")
            elif int(json_data["winner"]) == 0:
                print("draw")
            else:
                print("you lose")
            exit(0)
        if print_waiting:
            print("waiting for the other player")
            print_waiting = False
        sleep(1)


async def play(session, game_id, player):

    while True:
        print("your turn ({}):".format("x" if player == 1 else "o"))

        user_input = input()
        user_input = user_input.strip()
        user_input = user_input.split(" ")
        if len(user_input) == 2:
            if user_input[0].isnumeric() and user_input[1].isnumeric:

                json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/play?game=" + str(game_id) + "&player=" + str(player) + "&x=" + str(user_input[0]) +"&y=" + str(user_input[1]))
                json_data = json.loads(json_response)

                if "status" in json_data:
                    if not json_data["status"] == "bad":
                        break

        print("invalid input")

    await waiting(session, game_id, player)


async def main():
    host = str(sys.argv[1])

    port = int(sys.argv[2])

    async with aiohttp.ClientSession() as session:
        json_response = await fetch(session, 'http://'+host+":"+str(port)+"/list")
        json_data = json.loads(json_response)

        player = 0
        game_id = 0

        print ("Uspesne pripojeni k hernímu serveru", host+":"+str(port))

        while True:
            json_response = await fetch(session, 'http://' + host + ":" + str(port) + "/list")
            json_data = json.loads(json_response)

            game_id = await list_games(json_data, session)

            if game_id.strip().isnumeric():
                print("Připojuji se ke hře {}...".format(game_id))
                player = 2
                try:
                    json_response = await fetch(session, 'http://' + host + ":" + str(port) + "/status?game=" + str(game_id))
                    json_data = json.loads(json_response)
                    if empty_board(json_data["board"]):
                        print ("Připojen ke hře id {}".format(game_id))
                        await waiting(session, game_id, player)
                    else:
                        print ("Připojení ke hře se nezdařilo.")
                except AssertionError:
                    print ("Připojení ke hře se nezdařilo.")

            elif game_id.strip() == "new":
                print ("Zadej nazev: ", end="", sep="")
                name = input()
                player = 1
                json_response = await fetch(session, 'http://' + host + ":" + str(port) + "/start?name="+str(name))
                json_data = json.loads(json_response)
                game_id = json_data["id"]
                print("Byla zalozena nova hra s id {}.".format(game_id))
                print("___\n___\n___")
                await play(session, game_id, player)
                break
            else:
                print ("Nekorektni vstup!")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

