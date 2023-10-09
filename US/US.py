# Author: Chen Dong
# DCN 2023 Fall 
# Lab 3

from flask import Flask, abort, request
from socket import *

app = Flask(__name__)

@app.route('/')

def initialize():
    return "Initialization Succeed"


@app.route('/fibonacci', methods = ["GET"], endpoint="fibonacci")
def us():
    arg = request.args
    if not arg.get("hostname") or not arg.get("fs_port") or not arg.get("number") or not arg.get("as_ip") or not arg.get("as_port"):
        abort(400)
    else:
        hostname = arg.get("hostname")
        as_port = arg.get("as_port")
        dnsMessage = "TYPE=A\n" + "NAME=" + hostname
        as_ip = arg.get("as_ip")
        address = (as_ip, int(as_port))
        uso = socket(AF_INET, SOCK_DGRAM)
        uso.sendto(dnsMessage.encode(), address)

        responseMessage, authoritativeAddress = uso.recvfrom(2048)
        response = responseMessage.decode().split('\n')
        for line in response:
            print(line)
            name, value = line.split('=')
            if name == 'VALUE':
                ip = value
                print(ip)
                break

        if ip != "0.0.0.0":
            return "The IP address is: " + ip
        else:
            return "No IP address"

app.run(host = '0.0.0.0',
        port = 8080,)