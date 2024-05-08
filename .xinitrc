#!/bin/sh

# to apply cursors themes 
xrdb ~/.Xresources

# hides X mouse cursor when you do not need it
unclutter &

# start qtile window manager
qtile start
