#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, https://github.com/treedust, and Helen Aquino
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        data_list = data.split("\r\n\r\n")[0] 
        # print(data_list)
        # Ex. "HTTP/1.1 301 Moved Permanently"
        status_code = int(data_list.splitlines()[0].split(" ")[1])
        return status_code

    def get_headers(self,data):
        # idk if I need this so far, since I haven't needed to call it :/
        headers = data.split("\r\n")
        return headers

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""

        # urllib.parse is OKAY for parsing URLs; https://docs.python.org/3/library/urllib.parse.html
        o = urlparse(url)
        # Get the host, port, and path
        host = o.hostname
        if o.port is None:
            port = 80
        else: 
            port = o.port

        if o.path == "":
            path = "/"
        else:
            path = o.path
        
        self.connect(host, port)
        request = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(path, host)
        self.sendall(request)

        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)

        print("Code: {}\nBody: {}".format(code, body))
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        o = urlparse(url)
        # Get the host, port, and path
        host = o.hostname
        if o.port is None:
            port = 80
        else: 
            port = o.port

        if o.path == "":
            path = "/"
        else:
            path = o.path
        
        self.connect(host, port)

        if args == None:
            content = ""
        else: 
            content = urlencode(args)

        request = "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n{}".format(path, host, len(content), content)
        self.sendall(request)

        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)

        print("Code: {}\nBody: {}".format(code, body))
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
