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

import sys
import docopt
from search import get_host
from prettycli import red, green, blue

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
    confirm_params(params, args['--override'], dummy_validate)
    print('execute replacement')

def remove_cmd(args):
    pass

def config_cmd(args):
    pass

""" Must return boolean, str """
def dummy_validate(params):
    print('validating.....')
    return True, None

def confirm_params(params, override, validate_fn):
    validated = False
    confirmed = False
    while not confirmed:
        if not override:
            while not validated:
                validated, details = validate_fn(params)
                if not validated:
                    print("Your parameters are invalid. Details: %s"%details)
                    if procede("Would you like to edit your params?"):
                        #edit file
                        pass
            print(green("Validation PASSED"))
        pretty = '\n'.join(['%s: %s'%(str(v[0]),str(v[1])) for v in params])
        print('\n%s\n'%pretty)
        confirmed = procede("Does this look right to you?")
        if not confirmed:
            pass
            #edit file

def procede(msg):
    reply = input("%s (%s/%s/%s) " % (msg,green('y'),red('n'),blue('q'))).lower()
    if reply in ['y', 'yes']:
        return True
    if reply in ['n', 'no']:
        return False
    exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass 
