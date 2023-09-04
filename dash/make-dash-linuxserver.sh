#!/bin/bash

rm -r output-dash-linuxserver
mkdir output-dash-linuxserver

    #-ss 5 -t 10 \
docker run --rm -it \
    -v $(pwd):/config \
    -v $(pwd)/../source:/source \
    linuxserver/ffmpeg \
    -i /source/bbb_sunflower_2160p_60fps_normal.mp4 \
    -map 0:v: -b:v:0 300k -s:v:0 512x288 -c:v:0 libx264 -profile:v:0 main -level:v:0 3 \
    -map 0:v: -b:v:1 300k -s:v:1 512x288 -c:v:1 libx265 -profile:v:1 main -level:v:1 3 \
    -map 0:v: -b:v:2 300k -s:v:2 512x288 -c:v:2 libx265 -profile:v:2 main -level:v:2 3 -tag:v:2 hvc1 \
    -map 0:v: -b:v:3 300k -s:v:3 512x288 -c:v:3 libvpx-vp9 \
    -map 0:a: -b:a:0 128k -c:a:0 aac \
    -map 0:a: -b:a:1 128k -c:a:1 libfdk_aac -profile:a:1 aac_he \
    -map 0:a: -b:a:2 128k -c:a:2 libfdk_aac -profile:a:2 aac_he_v2 -ac:a:2 2 \
    -map 0:a: -b:a:3 320k -c:a:3 ac3 \
    -map 0:a: -b:a:4 320k -c:a:4 eac3 \
    -bf 1 -keyint_min 120 -g 120 -sc_threshold 0 \
    -b_strategy 0 -use_timeline 1 -use_template 1 \
    -adaptation_sets "id=0,streams=0 id=1,streams=1 id=2,streams=2 id=3,streams=3 id=4,streams=4 id=5,streams=5 id=6,streams=6 id=7,streams=7 id=8,streams=8" \
    -f dash /config/output-dash-linuxserver/manifest.mpd
