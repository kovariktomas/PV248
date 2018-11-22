import sys
import json
import http.client
import socket
import ssl



from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

def client_obsluha(upstream = sys.argv[2], timeout_set=1):
    socket.setdefaulttimeout(timeout_set)
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        conn = http.client.HTTPSConnection(upstream, context = ssl._create_unverified_context(), timeout=timeout_set)
        conn.request("GET", "/")

        r1 = conn.getresponse()
        headers = r1.getheaders()
        code = r1.status
        data1 = r1.read().decode("utf-8", "ignore")
        conn.close()
        return data1, headers, code
    except:
        data1 = None
        code = None
        headers = None
        conn.close()
        return data1, headers, code


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        data1, headers, code = client_obsluha()
        rows = {}
        if not code == None:
            rows["code"] = int(code)
            row = {}
            for header in headers:
                row[header[0]] = header[-1]
            rows["headers"] = row
            #print(data1)#.decode('UTF-8', "replace"))
            try:
                j = json.loads(data1.replace("\n", "").replace("\\", ""))
                rows["json"] = j
            except json.decoder.JSONDecodeError:
                j = None
            if j == None:
                rows["content"] = data1
        else:
            rows["code"] = "timeout"

        dataForJson = rows

        json_string = str(json.dumps(dataForJson))#, sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_string)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(json.dump(dataForJson, sys.stdout, indent=4, ensure_ascii=False))
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

def main():
    port = int(sys.argv[1])
    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

main()