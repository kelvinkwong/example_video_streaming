#!/bin/bash

rm -r output-dash
mkdir output-dash

# notes: 
# avc1.4d401e = -c:v:0 libx264 -profile:v:0 main -level:v:0 3

# -ss 5 -t 10 \
# -window_size 5 \
ffmpeg -i ./source/bbb_sunflower_2160p_60fps_normal.mp4 \
-map 0:v: -b:v:0 300k -s:v:0 512x288 -c:v:0 libx264 -profile:v:0 main -level:v:0 3 \
-map 0:v: -b:v:1 300k -s:v:1 512x288 -c:v:1 libx265 -profile:v:1 main -level:v:1 3 \
-map 0:v: -b:v:2 300k -s:v:2 512x288 -c:v:2 libx265 -profile:v:2 main -level:v:2 3 -tag:v:2 hvc1 \
-map 0:v: -b:v:3 300k -s:v:3 512x288 -c:v:3 libvpx-vp9 \
-map 0:a: -b:a:0 128k -c:a:0 aac -ar:a:0 48000 \
-map 0:a: -b:a:1 320k -c:a:1 ac3 -ar:a:1 48000 \
-map 0:a: -b:a:2 320k -c:a:2 eac3 -ar:a:2 48000 \
-bf 1 -keyint_min 120 -g 120 -sc_threshold 0 \
-b_strategy 0 -use_timeline 1 -use_template 1 \
-adaptation_sets "id=0,streams=0 id=1,streams=1 id=2,streams=2 id=3,streams=3 id=4,streams=4 id=5,streams=5 id=6,streams=6" \
-f dash ./output-dash/manifest.mpd
