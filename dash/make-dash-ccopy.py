#!/usr/bin/env python3

import subprocess
import os
import shutil
import glob
import pprint

HOST_SOURCE_DIR = "../docs/videos/single"
HOST_OUTPUT_DIR = "output-dash"
DOCKER_SOURCE_DIR = '/source'
DOCKER_OUTPUT_DIR = "/" + HOST_OUTPUT_DIR

if os.path.isdir(HOST_OUTPUT_DIR):
    shutil.rmtree(HOST_OUTPUT_DIR, ignore_errors=False)
os.mkdir(HOST_OUTPUT_DIR)

source_files = [file for file in glob.glob(HOST_SOURCE_DIR + "/*.mp4")]
source_files += [file for file in glob.glob(HOST_SOURCE_DIR + "/*.webm")]
source_files = [DOCKER_SOURCE_DIR + '/' + os.path.basename(file) for file in source_files]
CWD=os.getcwd()

# build adapations map
adaptations = [f'id={index},streams={index}' for index, _ in enumerate(source_files)]

command = ['docker', 'run', '--rm', '-it']

# docker source directories
command.extend(['-v', f'{CWD}/{HOST_SOURCE_DIR}:{DOCKER_SOURCE_DIR}'])
command.extend(['-v', f'{CWD}/{HOST_OUTPUT_DIR}:{DOCKER_OUTPUT_DIR}'])

command.extend(['linuxserver/ffmpeg', '-y'])

# trim
command.extend(['-ss', '5', '-t', '5'])

# add source files
for file in source_files:
    command.extend(['-i', file])

# include sources for output
for index, _ in enumerate(source_files):
    command.extend(['-map', f'{index}'])

# assume input is preencoded
command.extend(['-c:v', 'copy', '-c:a', 'copy'])

# dash manifest settings
command.extend(['-bf', '1'])
command.extend(['-keyint_min', '120'])
command.extend(['-g', '120'])
command.extend(['-sc_threshold', '0'])
command.extend(['-b_strategy', '0'])
command.extend(['-use_timeline', '1'])
command.extend(['-use_template', '1'])

# options to include in the manifest
command.extend(['-adaptation_sets', " ".join(adaptations)])

# output directory
command.extend(['-f', 'dash', f'/{DOCKER_OUTPUT_DIR}/manifest.mpd'])

print(command)
result = subprocess.run(command, capture_output=True)
pprint.pprint(result)
if b'No such file or directory' in result.stdout or \
    b"Invalid" in result.stdout:
        print('ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
        print('stdout==============================================================================================================')
        print(result.stdout.decode('utf-8'))
        print('stderr==============================================================================================================')
        print(result.stderr.decode('utf-8'))
        exit(1)
