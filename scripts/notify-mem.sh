#!/bin/bash

export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"
freemem=$(cat /proc/meminfo | awk '$1 == "MemFree:" {free=sprintf("%.2f", ($2/1024) / 1024); print free}' | head -n 1)
threshold=13.9

if [ $? -eq 0 ]; then
  if (($(echo "$freemem > $threshold" | bc -l))); then
    notify-send -u critical "Notify mem" "You memmory is kinda getting full"
  fi
else
  notify-send -u critical "Notify mem" "Something went wrong"
fi
