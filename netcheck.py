#!/usr/bin/python
#
# Netchecker
# Use: ./netcheck.py <path-to-file>
#
import sys
import socket
import time

# Check DNS
def dns(host):
    try:
        socket.gethostbyname(host)
        return 0
    except socket.error:
        return 1

# Check connection and get socket.error
def alive(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        translate = socket.gethostbyname(host)
        test = s.connect_ex((translate, port))
        return test
    except socket.error:
        return 1

file = open(sys.argv[1], "r")
errors = {
    1 : "Unknown socket.error",
    104 : "Connection rejected",
    110 : "Timeout",
    111 : "Service not running"
}

for line in file:
    if line[0] == "#":
        continue
    host = line.split(":")[0]
    port = int(line.split(":")[1])
    init = time.time()
    testdns = dns(host)
    testalive = alive(host, port)

    if (dns(host) == 1):
        end = time.time()
        print ("{0}:{1} | DNS record does not exist | {2}s").format(host, port, round((end - init), 3))
    else:
        if (testalive == 0):
            end = time.time()
            print ("{0}:{1} | Success | {2}s").format(host, port, round((end - init), 3))
        else:
            end = time.time()
            print ("{0}:{1} | {2} | {3}s").format(host, port, errors[testalive], round((end - init), 3))
