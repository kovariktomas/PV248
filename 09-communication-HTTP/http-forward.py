import sys
import json
import asyncio.subprocess
import http.server
import http.client
from aiohttp import web

#import ssl


def main():
    port = sys.argv[1]

    print(port)


main()