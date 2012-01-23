#!/usr/bin/env python2.6
# -*- encoding: utf-8 -*-
#
# rest-api for mantrid configuration
# work as a wrapper between mantrid rest-api and kapsi client
#

import ident
from urlparse import parse_qs

# kuka käyttäjä on?
def auth(data):
    #yield "%s " % data
    i = ident.getIdent(data['REMOTE_ADDR'],data['SERVER_PORT'],data['REMOTE_PORT'])
    if str(i) != "":
        return str(i)
    else:
        return False

def add_testdomain(name=""):
    if name == "":
        "".strip()
        #keksinimitähän
    raise NotImplementedError

def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    try:
        content_length = int(environ['CONTENT_LENGTH'])
    except KeyError:
        content_length = 0
    postdata = str(environ.get('wsgi.input').read(content_length))
    try:
        post = dict([p.split("=") for p in postdata.split("&")])
    except ValueError:
        yield "parametrivirhe".encode("utf-8")
        return
    get = parse_qs(environ.get("QUERY_STRING").encode("iso-8859-1").decode("utf-8", "replace"))
    user = auth(environ)
    if user != False:
        yield "user = %s" % user
        if environ["PATH_INFO"] == "/add/":
            if "name" in post:
                add_testdomain(post["name"])
            else:
                add_testdomain()
    else:
        yield "Tunnistautuminen epäonnistui!!"
