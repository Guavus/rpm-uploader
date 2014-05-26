#!/usr/bin/python
import os
import sys
import json
import subprocess
import argparse
import socket
from bottle import route, request, static_file, run, response

configs={}

@route('/upload', method='POST')
def do_upload():
    global configs
    data = request.files.data
    project = request.query.get('dir')
    if not data or not data.file:
        response.status = 400
        return dict(message='Missing parameters')

    output_dir = os.path.join(configs['output_dir'], *project.split('/'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, data.filename)
    if os.path.exists(file_path):
        response.status = 400
        return dict(message='File ' + file_path + ' already exists')

    # Save file
    data.save(file_path)

    # Update repo
    subprocess.call([configs['createrepo'], '-p', '--update', output_dir])

    return dict(result="Success", message="Ok")
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir')
    parser.add_argument('--port', default='1234', type=int)
    parser.add_argument('--createrepo', default='/usr/bin/createrepo')
    configs = vars(parser.parse_args(sys.argv[1:]))

    #Run server
    print "Starting on port %s. Will save in %s and run %s in repo." % (configs['port'], configs['output_dir'], configs['createrepo'])
    run(host=socket.gethostname(), port=configs['port'])

if __name__ == '__main__':
    main()
