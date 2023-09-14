#!/bin/bash

rm -r output-dash-linuxserver
mkdir output-dash-linuxserver

docker run --rm -it \
    -v $(pwd):/config \
    -v $(pwd)/../source:/source \
    linuxserver/ffmpeg \
    -ss 5 -t 10 \
    -i /source/bbb_sunflower_2160p_60fps_normal.mp4 \
    -b:v 200k -s:v 480x270 \
    -map 0:v: -c:v:0 libx264 -profile:v:0 main -level:v:0 3 \
    -map 0:v: -c:v:1 libx265 -profile:v:1 main -level:v:1 3 \
    -map 0:v: -c:v:2 libx265 -profile:v:2 main -level:v:2 3 -tag:v:2 hvc1 \
    -map 0:v: -c:v:3 libvpx \
    -map 0:v: -c:v:4 libvpx-vp9 \
    -b:a 64k \
    -map 0:a: -c:a:0 aac -b:a:0 128k \
    -map 0:a: -c:a:1 libfdk_aac -profile:a:1 aac_he \
    -map 0:a: -c:a:2 libfdk_aac -profile:a:2 aac_he_v2 -ac:a:2 2 \
    -map 0:a: -c:a:3 copy -b:a:3 320k \
    -map 0:a: -c:a:4 eac3 -b:a:4 320k \
    -map 0:a: -c:a:5 libvorbis -ac:a:5 2 \
    -map 0:a: -c:a:6 libopus -ac:a:6 2 \
    -bf 1 -keyint_min 120 -g 120 -sc_threshold 0 \
    -b_strategy 0 -use_timeline 1 -use_template 1 \
    -adaptation_sets "id=0,streams=0 id=1,streams=1 id=2,streams=2 id=3,streams=3 id=4,streams=4 id=5,streams=5 id=6,streams=6 id=7,streams=7 id=8,streams=8 id=9,streams=9 id=10,streams=10 id=11,streams=11" \
    -f dash /config/output-dash-linuxserver/manifest.mpd
