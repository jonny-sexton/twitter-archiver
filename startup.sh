#!/bin/bash

# twitter-crawler-1
sleep 1m
tmux new-session -d -s twitter-crawler-1
tmux send-keys -t twitter-crawler-1 "python3 /home/pi/main.py Tyson_Fury 2011-01-01 2021-01-01 keys/twitter_keys_1.yaml" Enter
