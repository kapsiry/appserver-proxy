#!/usr/bin/env python
# encoding: utf-8
# ident fetcher for appserver-proxy
#

import socket
import sys

def getIdent(server, myport, remoteport):

    HOST = server             # The remote host
    PORT = 113
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error, msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error, msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        return
    s.send("%s, %s\n" % (myport, remoteport))
    data = s.recv(1024)
    s.setblocking(0)
    s.settimeout(10)
    s.close()
    if data.split(":")[2].strip() == "UNIX":
        return data.split(":")[3].strip()
    else:
        return
