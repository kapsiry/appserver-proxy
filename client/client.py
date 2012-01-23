#!/usr/bin/env python
# encoding: UTF-8

import random
import sys
import os.path
import requests

BASE_URI = 'https://apps.example.com/apps/v1/'
USAGE = """Usage: kapsi-proxy <command> [options]

Commands:

  status        List your applications
  create        Create a new application
    --host www.mydomain.tld     Set up for a custom domain
  destroy <name>
"""

script_dir, script_name = os.path.split(__file__)
wordlist_file = os.path.join(script_dir, 'wordlist.txt')
with open(wordlist_file) as f:
    WORDS = [x.strip() for x in f]

def testname():
    word1 = random.choice(WORDS)
    word2 = random.choice(WORDS)
    number = random.randint(1000,9999)
    return "{}-{}-{}".format(word1, word2, number)

def print_apps(args):
    raise NotImplementedError

def add_app(args):
    if len(args) == 0:
        name = testname()
    elif len(args) == 1:
        name = args[0]
    else:
        raise Exception("Too many parameters")
    print "Adding", name
    r = requests.post(BASE_URI + 'add', data=dict(name=name))
    print testname()

def cmd_usage(args):
    print USAGE
    sys.exit(1)

def main():
    args = sys.argv[1:]
    f = cmd_usage
    cmds = {
        '-h': cmd_usage, '--help': cmd_usage, 'help': cmd_usage,
        'create': add_app,
        'add': add_app,
        'status': print_apps,
        'list': print_apps,
        }
    f = cmds.get(args[0], cmd_usage)
    if len(args) > 0:
        try:
            f(args[1:])
            sys.exit(0)
        except Exception, e:
            print e.__class__.__name__, unicode(e)
            sys.exit(1)
    else:
        cmd_usage(None)

if __name__ == '__main__':
    main()
