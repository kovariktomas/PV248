import sys
import json
import http.client
import socket
import ssl

from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

def client_obsluha(upstream = sys.argv[2], timeout_set=1, headers_to_set=None, method="GET"):
    upstream = upstream.replace("http://", "")
    upstream = upstream.replace("https://", "")
    upstream = upstream.split('/', 1)


    socket.setdefaulttimeout(timeout_set)
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        if headers_to_set == None:
            headers_to_set = {}
        #print (upstream)
        conn = http.client.HTTPSConnection(upstream[0], context = ssl._create_unverified_context(), timeout=timeout_set)
        if len(upstream)==2:
            conn.request(method, "/"+upstream[-1], headers=headers_to_set)
        else:
            conn.request(method, "/",  headers=headers_to_set)

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
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        #print ("in post method")
        rows = {}
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()
        try:
            data = json.loads(self.data_string)
            #print(data)
            #print(type(data))
            if data["type"]:
                type = data["type"]
            else:
                type = "GET"

            if data["timeout"]:
                timeout = int(data["timeout"])
            else:
                timeout = 1

            if data["headers"]:
                headers_to_set = data["headers"]
            else:
                headers_to_set = None

            data1, headers, code = client_obsluha(data["url"], timeout, headers_to_set, type)

            if not code == None:
                rows["code"] = int(code)
                row = {}
                for header in headers:
                    row[header[0]] = header[-1]
                rows["headers"] = row
                # print(data1)#.decode('UTF-8', "replace"))
                try:
                    j = json.loads(data1.replace("\n", "").replace("\\", ""))
                    rows["json"] = j
                except json.decoder.JSONDecodeError:
                    j = None
                if j == None:
                    rows["content"] = data1
            else:
                rows["code"] = "timeout"
        except:
            rows["code"] = "invalid json"

        dataForJson = rows

        json_string = str(json.dumps(dataForJson))  # , sys.stdout, indent=4, ensure_ascii=False))
        json_string = bytes(json_string, 'utf-8')
        self.wfile.write(json_string)
        return


def main():
    port = int(sys.argv[1])
    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

main()