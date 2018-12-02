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

def create_handler():
    class Handler(CGIHTTPRequestHandler):
        def do_GET(self):
            params = str(self.path).split("?", 1)[-1]
            request_path = urllib.parse.urlparse(self.path).path
            local_cgi_path = sys.argv[2] + request_path[1:]
            if os.path.isfile(local_cgi_path):
                suffix = ".cgi";
                if local_cgi_path.endswith(suffix):
                    self.cgi_info = '', local_cgi_path
                    self.run_cgi()
                else:
                    with open(local_cgi_path, 'rb') as f:
                        self.send_response(200)
                        self.send_header("Content-Type", 'application/octet-stream')
                        self.send_header("Content-Disposition",
                                         'attachment; filename="{}"'.format(os.path.basename(local_cgi_path)))
                        fs = os.fstat(f.fileno())
                        self.send_header("Content-Length", str(fs.st_size))
                        self.end_headers()
                        shutil.copyfileobj(f, self.wfile)
            elif os.path.isdir(local_cgi_path):
                try:
                    dirs = os.listdir(local_cgi_path)
                    html_code = ""
                    html_code = """<html>
                        <head>
                            <title> Index of"""
                    html_code += str(local_cgi_path)
                    html_code += """</title>
                         </head>
                         <body>
                            <h1> Index of """
                    html_code += str(local_cgi_path)
                    html_code += """</h1>
                            <ul>"""

                    for file in dirs:
                        html_code += """<li>
                                    <a href=\""""
                        suffix = "/"
                        if local_cgi_path.endswith(suffix):
                            html_code += str(local_cgi_path) + str(file)
                        else:
                            html_code += str(local_cgi_path) + "/" + str(file)
                        html_code += """\">"""
                        html_code += str(file)
                        html_code += """</a></li>"""

                    html_code += """</ul>
                            </body>
                        </html>"""

                    self.send_response(200)
                    self.send_header("Content-Length", len(html_code))
                    self.send_header("Content-Type", 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(bytes(html_code, "utf-8"))
                except IOError:
                    self.send_error(404, 'file not found')
            else:
                self.send_error(404, 'file not found')
        def do_POST(self):
            load = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            request_path = load["content"]+"/"
            local_cgi_path = sys.argv[2] + request_path[1:]
            if os.path.isfile(local_cgi_path):
                suffix = ".cgi"
                if local_cgi_path.endswith(suffix):
                    self.cgi_info = '', local_cgi_path
                    self.run_cgi()
                else:
                    with open(local_cgi_path, 'rb') as f:
                        self.send_response(200)
                        self.send_header("Content-Type", 'application/octet-stream')
                        self.send_header("Content-Disposition",
                                         'attachment; filename="{}"'.format(os.path.basename(local_cgi_path)))
                        fs = os.fstat(f.fileno())
                        self.send_header("Content-Length", str(fs.st_size))
                        self.end_headers()
                        shutil.copyfileobj(f, self.wfile)
            elif os.path.isdir(local_cgi_path):
                try:
                    dirs = os.listdir(local_cgi_path)
                    html_code = ""
                    html_code = """<html>
                                    <head>
                                        <title> Index of"""
                    html_code += str(local_cgi_path)
                    html_code += """</title>
                                     </head>
                                     <body>
                                        <h1> Index of """
                    html_code += str(local_cgi_path)
                    html_code += """</h1>
                                        <ul>"""

                    for file in dirs:
                        html_code += """<li>
                                                <a href=\""""
                        suffix = "/"
                        if local_cgi_path.endswith(suffix):
                            html_code += str(local_cgi_path) + str(file)
                        else:
                            html_code += str(local_cgi_path) + "/" + str(file)
                        html_code += """\">"""
                        html_code += str(file)
                        html_code += """</a></li>"""

                    html_code += """</ul>
                                        </body>
                                    </html>"""

                    self.send_response(200)
                    self.send_header("Content-Length", len(html_code))
                    self.send_header("Content-Type", 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(bytes(html_code, "utf-8"))
                except IOError:
                    self.send_error(404, 'file not found')
            else:
                self.send_error(404, 'file not found')
    return Handler

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    port = int(sys.argv[1])
    dir = str(sys.argv[2])

    h = create_handler()
    server = ThreadedHTTPServer(('127.0.0.1', int(sys.argv[1])), h)

    print ('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

main()



