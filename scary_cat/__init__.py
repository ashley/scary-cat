#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""scary-cat is a command line tool for doing scary things.
Usage:
    scary-cat replace <host-id> [--override]
    scary-cat replace-many <input-file> <instance-type>
    scary-cat remove <host-id> [--override]
    scary-cat remove [--many] [--override]
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
from subprocess import Popen, check_output
import os

from .search import get_host, get_dependencies
from .instance import Provision, RemoveHosts

def main():
    args = docopt.docopt(__doc__, version="1.0")
    if args['replace']:
        return replace_cmd(args) 
    elif args['replace-many']:
        return replace_many_cmd(args) 
    elif args['remove']:
        return remove_cmd(args)
    elif args['config']:
        return config_cmd(args)
    else:
        print("Invalid command")
        return

def remove_cmd(args):
    params = RemoveHosts()
    if args['<host-id>']:
        params.nodes = args['<host-id>']
    params = edit_file(params, RemoveHosts,  ask_edit=False)
    params = confirm_params(params, RemoveHosts, args['--override'])
    print(blue('removing nodes...'))
    jenkins_build('remove-node-prod', params)    

def replace_cmd(args):
    # Find Host Information in datadog
    params = get_host(args['<host-id>'])
    params = confirm_params(params,Provision, args['--override'])
    print(blue('execute replacement...'))
    jenkins_build('provision-consumer-prod', params) 

def replace_many_cmd(args):
    # Find Host Information in datadog
    f = open(args['<input-file>'], "r")
    for host in f:
        params = get_host(host)
        if args['<instance-type>']:
            params.instance_size = args['<instance-type>']
        params.additional_tags = 'newbatch:true'
        params = confirm_params(params,Provision, False)
        print(blue('execute replacement...'))
        jenkins_build('provision-consumer-prod', params)

def config_cmd(args):
    options = get_dependencies()
    for k, v in options.items():
        print("%s: %s" % (k,v))
    if os.getenv("JENKINS_URL"):
        print("JENKINS_URL: %s" % os.getenv("JENKINS_URL"))
    else:
        print(red("Failed to get JENKINS_URL. Be sure to have it set as an environment variable"))

def jenkins_build(job, params):
    args = ['jinkies', 'build', job, '--no-log']
    args += ['{}={}'.format(tag[0], tag[1]) for tag in params.as_tuples()]
    return check_output(args)

def edit_file(params, cmd_type, ask_edit=True):
    if ask_edit:
        if not procede("Would you like to edit your params?"):
            return params
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
        box = cmd_type(params)
    except:
        print(red("There was an error with your edits."))
        raise
    assert box != None
    return box
    

def confirm_params(params, cmd_type, override):
    validated = False
    confirmed = False
    while not confirmed:
        if not override:
            while not validated:
                validated, details = params.validate()
                if not validated:
                    print(red("Your parameters are invalid. Details: %s"%details))
                    params = edit_file(params, cmd_type)
                    validated = False
            print(green("Validation PASSED"))
        print(params)
        confirmed = procede("Does this look right to you?")
        if not confirmed:
            params = edit_file(params, cmd_type)
            validated = False
    return params

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
