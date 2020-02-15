#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""scary-cat is a command line tool for doing scary things.
Usage:
    scary-cat replace <host-id> [--override]
    scary-cat remove <host-id> [--many] [--override]
    scary-cat config

Options:
    -h --help       Show this help.
    --override   Override parameter linter (NOT recommended).
    --many       Add multiple host IDs using an editor
    --version       Show version and exit.
"""
from __future__ import absolute_import
import sys
import docopt
from prettycli import red, green, blue
import click

from .search import get_host, Provision

def main():
    args = docopt.docopt(__doc__, version="1.0")
    if args['replace']:
        return replace_cmd(args) 
    elif args['remove']:
        print()
    elif args['config']:
        print()
    else:
        print("Invalid command")
        return

def replace_cmd(args):
    # Find Host Information in datadog
    params = get_host(args['<host-id>'])
    confirm_params(params, args['--override'])
    print('execute replacement')

def remove_cmd(args):
    pass

def config_cmd(args):
    pass

def edit_file(params):
    if procede("Would you like to edit your params?"):
        MARKER = '# Everything below is ignored'
        edited = click.edit(str(params)+'\n'+MARKER)
        if edited is None:
            return params
        try:
            tag_lines = edited.split('\n')
            ignore_index = len(tag_lines)
            for i in range(len(tag_lines)):
                if tag_lines[i] == MARKER:
                    ignore_index = i
                    break
            tag_lines = tag_lines[:ignore_index]
            params = [tag.split(': ') for tag in tag_lines]
            box = Provision(params)
        except:
            print(red("There was an error with your edits."))
            raise
        assert box != None
        return box
    return params
    

def confirm_params(params, override):
    validated = False
    confirmed = False
    while not confirmed:
        if not override:
            while not validated:
                validated, details = params.validate()
                if not validated:
                    print("Your parameters are invalid. Details: %s"%details)
                    params = edit_file(params)
                    validated = False
            print(green("Validation PASSED"))
        print(params)
        confirmed = procede("Does this look right to you?")
        if not confirmed:
            params = edit_file(params)
            validated = False

def procede(msg):
    reply = input("%s (%s/%s/%s) " % (msg,green('y'),red('n'),blue('q'))).lower()
    if reply in ['y', 'yes']:
        return True
    if reply in ['n', 'no']:
        return False
    exit()

if __name__ == '__main__':
    try:
        print(__name__)
        main()
    except KeyboardInterrupt:
        pass 
