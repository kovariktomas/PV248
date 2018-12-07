import pygame
from pygame.locals import *
import time
import pygame
import time
import random
import sys
import json
import http.client
import socket
import ssl
import aiohttp
import asyncio
from time import sleep



pygame.init()
display_width = 600
display_height = 625
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0,255,0)
block_color = (53, 115, 255)
car_width = 73
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()

status_game = -1
winner = None


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


async def game_intro(session):
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects("Tic Tac Toe", largeText)
        TextRect.center = ((display_width / 2), (20))
        gameDisplay.blit(TextSurf, TextRect)

        largeText = pygame.font.Font('freesansbold.ttf', 17)
        TextSurf, TextRect = text_objects("Dostupné hry na serveru: ", largeText)
        TextRect.center = ((140), (50))


        gameDisplay.blit(TextSurf, TextRect)

        await list_games(session)

        pygame.display.update()
        clock.tick(15)


async def button(msg,x,y,w,h,ic,ac,gameDisplay, action=None, params=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            if not params == None:
                if len(params) == 3:
                    await action(params[0],  params[1], params[2])
                elif len(params) == 1:
                    await action(params[0])
            else:
                await action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

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


def print_board(board, board_gui):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 1:
                drawMove(board_gui, i, j, 1)
            if board[i][j] == 2:
                drawMove(board_gui, i, j, 2)



# declare our support functions

def initBoard():
    gameDisplay = pygame.display.set_mode((600, 625))
    background = pygame.Surface(gameDisplay.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # draw the grid lines
    # vertical lines...
    pygame.draw.line(background, (0, 0, 0), (200, 0), (200, 600), 2)
    pygame.draw.line(background, (0, 0, 0), (400, 0), (400, 600), 2)

    # horizontal lines...
    pygame.draw.line(background, (0, 0, 0), (0, 200), (600, 200), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 400), (600, 400), 2)

    # return the board
    return background


async def gameWon(board, board_gui, session):

    global winner

    # check for winning rows
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2]) and not (board[i][0] == 0):
            pygame.draw.line(board_gui, (250, 0, 0), (0, (i + 1) * 200 - 100), (600, (i + 1) * 200 - 100), 2)
            params = []
            params.append(session)
            await button(str("Go back"), 460, 420, 100, 50, green, bright_green, board_gui, game_intro, params)

            break
        elif (board[0][i] == board[1][i] == board[2][i]) and not (board[0][i] == 0):
            pygame.draw.line(board_gui, (250, 0, 0), ((i + 1) * 200 - 100, 0), ((i + 1) * 200 - 100, 600), 2)
            params = []
            params.append(session)
            await button(str("Go back"), 460, 420, 100, 50, green, bright_green, board_gui, game_intro, params)
            break

    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and not (board[0][0] == 0):
        pygame.draw.line(board_gui, (250, 0, 0), (50, 50), (540, 540), 2)
        params = []
        params.append(session)
        await button(str("Go back"), 460, 420, 100, 50, green, bright_green, board_gui, game_intro, params)

    if (board[0][2] == board[1][1] == board[2][0]) and not (board[0][2] == 0):
        pygame.draw.line(board_gui, (250, 0, 0), (540, 50), (50, 540), 2)
        params = []
        params.append(session)
        await button(str("Go back"),460, 420, 100, 50, green, bright_green, board_gui, game_intro, params)


async def drawStatus(session, game_id, player, board):

    json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/status?game=" + str(game_id))
    json_data = json.loads(json_response)

    if "next" in json_data:
        print_board(json_data["board"], board)
        if int(json_data["next"]) == player:
            message = "your turn ({}):".format("x" if player == 1 else "o")
            global status_game
            status_game = player
        else:
            message = "waiting for the other player"
    elif "winner" in json_data:
        print_board(json_data["board"], board)
        await gameWon(json_data["board"], board, session)
        global winner
        winner = json_data["winner"]
        if int(json_data["winner"]) == player:
            message = "you win"
        elif int(json_data["winner"]) == 0:
            message = "draw"
        else:
            message = "you lose"

    # render the status message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    # copy the rendered message onto the board
    board.fill((250, 250, 250), (0, 600, 600, 25))
    board.blit(text, (10, 600))


async def showBoard(session, game_id, player, board):
    await drawStatus(session, game_id, player, board)
    gameDisplay.blit(board, (0, 0))
    pygame.display.update()


def boardPos(mouseX, mouseY):
    if (mouseY < 200):
        row = 0
    elif (mouseY < 400):
        row = 1
    else:
        row = 2

    if (mouseX < 200):
        col = 0
    elif (mouseX < 400):
        col = 1
    else:
        col = 2
    return (row, col)


def drawMove(board, boardRow, boardCol, player):
    centerX = ((boardCol) * 200) + 100
    centerY = ((boardRow) * 200) + 100
    if (player == 2):
        pygame.draw.circle(board, (0, 0, 0), (centerX, centerY), 88, 2)
    else:
        pygame.draw.line(board, (0, 0, 0), (centerX - 70, centerY - 70), \
                         (centerX + 70, centerY + 70), 2)
        pygame.draw.line(board, (0, 0, 0), (centerX + 70, centerY - 70), \
                         (centerX - 70, centerY + 70), 2)


async def clickBoard(session, game_id, player, board):
    global status_game
    if status_game == player:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (row, col) = boardPos(mouseX, mouseY)

        json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/play?game=" + str(game_id) + "&player=" + str(player) + "&x=" + str(row) + "&y=" + str(col))
        json_data = json.loads(json_response)

        if "status" in json_data:
            if not json_data["status"] == "bad":
                drawMove(board, row, col, player)
    else:
        return


async def play_game(session, game_id, player):
    # create the game board
    board = initBoard()

    # main event loop
    running = 1

    while (running == 1):
        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0
            elif event.type is MOUSEBUTTONDOWN:
                # the user clicked; place an X or O
                await clickBoard(session, game_id, player,board)

            # update the display
        await showBoard(session, game_id, player, board)
        clock.tick(15)


    exit(0)


async def new_game():
    async with aiohttp.ClientSession() as session:
        name = "Game name"
        player = 1
        json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2])  + "/start?name=" + str(name))
        json_data = json.loads(json_response)
        game_id = json_data["id"]

        await play_game(session, game_id, player)


async def list_games(session):
    json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/list")
    json_data = json.loads(json_response)
    json_data_tmp = json_data
    i = 0
    for game in json_data:
        json_response = await fetch(session, 'http://' + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/status?game=" + str(game["id"]))
        json_data = json.loads(json_response)
        if "board" in json_data:
            if empty_board(json_data["board"]):
                #print ("{} \t\t {}".format(game["id"], game["name"]))
                params = []
                params.append(session)
                params.append(game["id"])
                params.append(2)
                await button(str("Connect to: " + str(game["id"]) + ": " + game["name"]), 50, 80+i, 480, 25, green, bright_green, gameDisplay, play_game, params)
                i += 30
                #break
    #print("Zadejte id hry, nebo zalozte novou hru napsanim \"new\": ", sep='', end='')

    await button(str("New game"), 460, 520, 100, 50, green, bright_green, gameDisplay, new_game)


async def main():
    host = str(sys.argv[1])

    port = int(sys.argv[2])

    async with aiohttp.ClientSession() as session:
        player = 0
        game_id = 0
        print ("Uspesne pripojeni k hernímu serveru", host+":"+str(port))
        await game_intro(session)


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except aiohttp.client_exceptions.ClientConnectorError:
    print ("chyba serveru zkuste to znovu")
    exit(0)