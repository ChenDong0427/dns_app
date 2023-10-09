# Author: Chen Dong
# DCN 2023 Fall 
# Lab 3
from flask import Flask, abort, Response, request
from socket import *

app = Flask(__name__)

@app.route('/')
def initialize():
    return "Initialization Succeed"

@app.route('/register', methods = ["PUT"], endpoint="register")
def fs():

    hostname = request.json.get("hostname")
    ip = request.json.get("ip")

    dm = "TYPE=A\n" + "NAME=" + hostname + "\nVALUE=" + ip + "\nTTL=10"
    address = (ip, 53533)

    fso = socket(AF_INET, SOCK_DGRAM)
    fso.sendto(dm.encode(), address)

    response, addr = fso.recvfrom(2048)
    print(response.decode())

    return Response("Registration Finished!", status=201)

@app.route('/fibonacci', methods = ["GET"], endpoint="fibonacci")
def fs():
    arg = request.args
    if not arg.get("number"):
        abort(400)
    num = arg.get("number")
    temp = [str(i) for i in range(10)]
    for character in num:
        if character not in temp:
            abort(400)
    num = int(num)

    def fib(n):
        a, b = 1, 1
        for i in range(n - 1):
            a, b = b, a + b
        return a

    return str(fib(num))

app.run(host = '0.0.0.0',
        port = 9090,
        debug = True)