#!/bin/bash

# command="curl -sL "$url" | grep --color=auto -e audio -e video"
command="grep --color=auto -e \<AdaptationSet -e \<Representation $1"
echo $command
eval $command
