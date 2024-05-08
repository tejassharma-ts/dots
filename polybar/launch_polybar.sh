#!/bin/bash

# polybar script to  to solve this issue https://www.reddit.com/r/qtile/comments/y4mayp/qtile_takes_over_the_polybar/

killall -q polybar

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar > /dev/null; do sleep 1; done

echo "---" | tee -a /tmp/main.log

if type "xrandr" > /dev/null; then	
    for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do		
        MONITOR=$m polybar --reload main -c ~/.config/polybar/config.ini & 2>&1 | tee -a /tmp/main.log & disown
    done
else
    polybar --reload main -c ~/.config/polybar/config.ini & 2>&1 | tee -a /tmp/main.log & disown
fi

echo "Bars launched..."
