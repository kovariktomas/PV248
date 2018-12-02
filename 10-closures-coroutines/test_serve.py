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
import re

async def get_handler(request):
    params = str(request.rel_url).split("?", 1)[-1]
    #params = params.split("&")
    request_path = urllib.parse.urlparse(request.path).path
    local_cgi_path = sys.argv[2]+request_path[1:]
    if os.path.isfile(local_cgi_path):
        # run cgi script
        try:
            result = subprocess.call(['chmod', '0777',local_cgi_path])
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
            result = subprocess.call(['chmod', '0777', local_cgi_path])
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


def main():
    port = int(sys.argv[1])
    dir = str(sys.argv[2])

    application = web.Application()
    application.add_routes([web.get('/{name:.*(.cgi|.Cgi|.CGI)$}', get_handler),
                            web.post('/{name:.*(.cgi|.Cgi|.CGI)$}', post_handler),
                            web.static("/", dir, show_index=True)])
    web.run_app(application, port=port)


main()