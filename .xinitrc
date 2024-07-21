#!/bin/sh

# to apply cursors themes 
xrdb ~/.Xresources

# hides X mouse cursor when you do not need it
unclutter &

xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
xrandr --dpi 96

# start qtile window manager
qtile start
