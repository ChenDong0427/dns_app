# Author: Chen Dong
# DCN 2023 Fall 
# Lab 3

from socket import *

aso = socket(AF_INET, SOCK_DGRAM)
aso.bind(('', 53533))

while True:
    message, ca = aso.recvfrom(2048)
    message = message.decode()

    print(message)

    length = message.split('\n')

    if len(length) == 2:
        t = 'Query'
    else:
        t = 'Register'
    for line in length:
        name, value = line.split('=')
        if name == "NAME":
            hostname = value
        elif name == "VALUE":
            ip = value
    if t == "Register":
        file = open("DNS.txt", "a+")
        file.write(message + '\n')
        file.close()

        response = b'Finished Registration!'
        aso.sendto(response, ca)
    else:
        ip = "0.0.0.0"
        with open("DNS.txt", "r") as f:
            line = f.readline()
            while line.strip() != "":
                if line.find(hostname) != -1:
                    line = f.readline()
                    name, value = line.split('=')
                    ip = value
                    break
                line = f.readline()

        rm = "TYPE=A\n" + "NAME=" + hostname + "\nVALUE=" + ip + "\nTTL=10"
        aso.sendto(rm.encode(), ca)
        print("Succeed")