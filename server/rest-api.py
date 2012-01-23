#!/usr/bin/env python2.6
# -*- encoding: utf-8 -*-
#
# rest-api for mantrid configuration
# works as a wrapper between mantrid rest-api and kapsi client.
#

import ident
from urlparse import parse_qs

def add_testdomain(name=""):
    if name == "":
        "".strip()
        #createnamehere
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
        yield "Parsing error!".encode("utf-8")
        return
    get = parse_qs(environ.get("QUERY_STRING").encode("iso-8859-1").decode("utf-8", "replace"))
    # ask ident  who you are
    user = ident.getIdent(environ['REMOTE_ADDR'],environ['SERVER_PORT'],environ['REMOTE_PORT'])
    if user is not None:
        yield "user = %s" % user
        if environ["PATH_INFO"] == "/add/":
            if "name" in post:
                add_testdomain(post["name"])
            else:
                add_testdomain()
    else:
        yield "Username not found"
