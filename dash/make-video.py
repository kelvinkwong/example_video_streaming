#!/usr/bin/env python3

import subprocess
import os
import shutil

print(os.getcwd())

OUTPUT_DIR="output-video"
shutil.rmtree(OUTPUT_DIR, ignore_errors=False)
os.mkdir(OUTPUT_DIR)
OUTPUT_DIR="/config/" + OUTPUT_DIR

command_strings="""
-map 0:v -c:v libx264 -b:v 200k -s:v 480x270 -profile:v main -level:v 3 $OUTPUT/libx264.mp4
-map 0:v -c:v libx264 -b:v 200k -s:v 480x270 -profile:v main -level:v 3 $OUTPUT/libx264.ts
-map 0:v -c:v libx265 -b:v 200k -s:v 480x270 -profile:v main -level:v 3 $OUTPUT/libx265.mp4
-map 0:v -c:v libx265 -b:v 200k -s:v 480x270 -profile:v main -level:v 3 $OUTPUT/libx265.ts
-map 0:v -c:v libvpx -b:v 200k -s:v 480x270 $OUTPUT/libvpx-vp8.webm
-map 0:v -c:v libvpx-vp9 -b:v 200k -s:v 480x270 $OUTPUT/libvpx-vp9.webm
-map 0:v -c:v libaom-av1 -b:v 200k -s:v 480x270 $OUTPUT/libaom-av1.mp4
-map 0:a -c:a aac -b:a 128k $OUTPUT/aac_lc.mp4
-map 0:a -c:a aac -b:a 128k $OUTPUT/aac_lc.ts
-map 0:a -c:a libfdk_aac -b:a 64k -profile:a aac_he $OUTPUT/aac_he.mp4
-map 0:a -c:a libfdk_aac -b:a 64k -profile:a aac_he_v2 -ac:a 2 $OUTPUT/aac_he_v2.mp4
-map 0:a -c:a ac3 -b:a 320k $OUTPUT/ac3.mp4
-map 0:a -c:a ac3 -b:a 320k $OUTPUT/ac3.ts
-map 0:a -c:a eac3 -b:a 320k $OUTPUT/eac3.mp4
-map 0:a -c:a eac3 -b:a 320k $OUTPUT/eac3.ts
-map 0:a -c:a libvorbis -b:a 64k -ac:a 2 $OUTPUT/libvorbis.webm
-map 0:a -c:a libopus -b:a 64k -ac:a 2 $OUTPUT/libopus.webm
"""

INPUT="-i /source/bbb_sunflower_2160p_60fps_normal.mp4"
TRIM="-ss 5 -t 5"
CWD=os.getcwd()
DEFAULT_COMMANDS=f"docker run --rm -it -v {CWD}:/config -v {CWD}/../source:/source linuxserver/ffmpeg -y {TRIM} {INPUT}"
DEFAULT_COMMANDS=f"docker run --rm -it -v {CWD}:/config -v {CWD}/../source:/source linuxserver/ffmpeg -y {INPUT}"

for command in command_strings.splitlines():
    filename = os.path.basename(command.split(' ').pop())
    osd = f"-vf drawtext=fontfile=/source/NotoSansMath-Regular.ttf:text={filename}:fontcolor=white:fontsize=300:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2"
    if command != "":
        _command = DEFAULT_COMMANDS
        if "0:v" in command:
            _command += " " + osd
        _command += " " + command.replace("$OUTPUT", OUTPUT_DIR)
        _command = _command.split(' ')
        print(_command)
        result = subprocess.run(_command, capture_output=True)
        if b"Invalid" in result.stdout:
            print('stdout==============================================================================================================')
            print(result.stdout.decode('utf-8'))
            print('stderr==============================================================================================================')
            print(result.stderr.decode('utf-8'))
            exit(1)
