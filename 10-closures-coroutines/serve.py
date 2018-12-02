import aiohttp
from aiohttp import web
import asyncio
import sys
import json
import os
import urllib.error
import urllib.parse
import http.server
import urllib.request
import logging
import subprocess
from subprocess import Popen, PIPE
import cgi
import datetime
import re


async def get_handler(request):
    params = str(request.rel_url).split("?", 1)[-1]
    #params = params.split("&")
    request_path = urllib.parse.urlparse(request.path).path
    local_cgi_path = sys.argv[2]+request_path[1:]
    if os.path.isfile(local_cgi_path):
        # run cgi script
        try:
            result = await subprocess.call(['chmod', '0777',local_cgi_path])
        except:
            pass

        tmp_path = local_cgi_path
        tmp_path = tmp_path + " '" + params +"'"
        p = Popen(tmp_path, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        output = output.decode("utf-8")
        content_type = re.compile("Content-type:(.*)?\n(.*)")
        m = content_type.match(output)
        if m:
            output = output.replace(str(m.group(0).strip()), "")
            return web.Response(body=str(output), content_type=str(m.group(1).strip()))  # return cgi vysledek
        else:
            return web.Response(body="Nevalidni cgi!", content_type="text/html")
    else:
        return web.Response(body="Soubor neexistuje!", content_type="text/html")



async def post_handler(request):

    request_path = urllib.parse.urlparse(request.path).path
    local_cgi_path = sys.argv[2] + request_path[1:]
    if os.path.isfile(local_cgi_path):
        # run cgi script
        try:
            result = await subprocess.call(['chmod', '0777', local_cgi_path])
        except:
            pass
        p = Popen([local_cgi_path, 'arg1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        output = output.decode("utf-8")
        content_type = re.compile("Content-type:(.*)?\n(.*)")
        m = content_type.match(output)
        if m:
            output = output.replace(str(m.group(0).strip()), "")
            return web.Response(body=str(output), content_type=str(m.group(1).strip()))  # return cgi vysledek
        else:
            return web.Response(body="Nevalidni cgi!", content_type="text/html")
    else:
        return web.Response(body="Soubor neexistuje!", content_type="text/html")


#def main():
#    port = int(sys.argv[1])
#    dir = str(sys.argv[2])

#    application = web.Application()
#    application.add_routes([web.get('/{name:.*(.cgi|.Cgi|.CGI)$}', get_handler),
#                            web.post('/{name:.*(.cgi|.Cgi|.CGI)$}', post_handler),
#                            web.static("/", dir, show_index=True)])
#    web.run_app(application, port=port)

#main()
queues = []

loop = asyncio.get_event_loop()

# Broadcast data is transmitted through a global Future. It can be awaited
# by multiple clients, all of which will receive the broadcast. At each new
# iteration, a new future is created, to be picked up by new awaiters.
broadcast_data = loop.create_future()

def broadcast(msg):
    global broadcast_data
    msg = str(msg)
    print(">> ", msg)
    if not broadcast_data.done():
        broadcast_data.set_result(msg)
    broadcast_data = loop.create_future()

# Dummy loop to broadcast the time every 5 seconds
async def broadcastLoop():
    while True:
        broadcast(datetime.datetime.now())
#       print('#',end='',flush=True)
        await asyncio.sleep(5)

# ws broadcast loop: Each WS connection gets one of these which waits for broadcast data then sends it
async def echo_loop(ws):
    while True:
        msg = await broadcast_data
        await ws.send_str(str(msg))

# web app shutdown code: cancels any open tasks and closes any open websockets
# Only partially working
async def on_shutdown(app):
    print('Shutting down:', end='')
    for t in app['tasks']:
        print('#', end='')
        if not t.cancelled():
            t.cancel()
    for ws in app['websockets']:
        print('.', end='')
        await ws.close(code=aiohttp.WSCloseCode.GOING_AWAY, message='Server Shutdown')
    print(' Done!')


#tcpServer = loop.run_until_complete(asyncio.start_server(handle_echo, '0.0.0.0', 8081, loop=loop))
#print('Serving on {}'.format(tcpServer.sockets[0].getsockname()))

# The application code:
def main():
    port = int(sys.argv[1])
    dir = str(sys.argv[2])

    app = web.Application()
    app['websockets'] = []
    app['tasks'] = []
    app.add_routes([web.get('/{name:.*(.cgi|.Cgi|.CGI)$}', get_handler),
                    web.post('/{name:.*(.cgi|.Cgi|.CGI)$}', post_handler),
                    web.static("/", dir, show_index=True)])
    app.on_shutdown.append(on_shutdown)

    # Kick off the 5s loop
    tLoop=loop.create_task(broadcastLoop())


    # Kick off the web/ws server
    async def start():
        global runner, site
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()

    async def end():
        await app.shutdown()

    loop.run_until_complete(start())

    # Main program "loop"
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # On exit, kill the 5s loop
        tLoop.cancel()
        # .. and kill the web/ws server
        loop.run_until_complete( end() )

    # Stop the main event loop
    loop.close()

if __name__ == '__main__':
    main()