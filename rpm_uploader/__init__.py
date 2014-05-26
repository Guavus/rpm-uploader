#!/usr/bin/python

from __future__ import (absolute_import, division, print_function, unicode_literals)
import sys
import os
import json
import subprocess
import argparse
import socket
from bottle import route, request, response, run


configs={}

@route('/upload', method='POST')
def upload():
    global configs
    input_data_files = request.files.getall('data')
    project = request.query.get('dir', '')

    if len(input_data_files) <= 0:
        if configs['verbose']:
            print('No file specified to upload')
        response.status = 400
        return dict(message='No file specified to upload')

    output_dir = os.path.join(configs['output_dir'], *project.split('/'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for data in input_data_files:
        file_path = os.path.join(output_dir, data.filename)
        if os.path.exists(file_path):
            if configs['verbose']:
                print('File already exists.')
            response.status = 400
            return dict(message='File ' + file_path + ' already exists. Will not overwrite')

        # Print
        if configs['verbose']:
            print("Uploading file(s) %s to folder %s." % (data.filename, output_dir))

        # Save file
        data.save(file_path)

    # Update repo
    subprocess.call(configs['createrepo'].split(" ") + [output_dir])

    return dict(result="Success", message="Ok")
    
def main():
    global configs
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir')
    parser.add_argument('--port', default='1234', type=int)
    parser.add_argument('--createrepo', default='/usr/bin/createrepo -p --update')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.add_argument('--silent', dest='verbose', action='store_false')

    parser.set_defaults(verbose=False)
    configs = vars(parser.parse_args(sys.argv[1:]))

    #Run server
    print("Starting on port %s. Will save in %s and run %s in repo." % (configs['port'], configs['output_dir'], configs['createrepo']))
    run(host=socket.gethostname(), port=configs['port'])

if __name__ == '__main__':
    main()
