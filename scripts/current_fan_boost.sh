#!/bin/bash

current_fan_value=$(cat /sys/devices/platform/asus-nb-wmi/fan_boost_mode)
echo "$current_fan_value"

if [ "$current_fan_value" -eq 1 ]; then
	notify-send "Asus Wmi" "Your laptop is rocking in Performance mode."
elif [ "$current_fan_value" -eq 0 ]; then
	notify-send "Asus Wmi" "Your laptop is rocking in Normal mode."
else
	notify-send "Asus Wmi" "Your laptop is rocking in Slient mode."
fi
