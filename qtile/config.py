from libqtile import bar, layout, hook, group, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

import os
import subprocess

mod = "mod4"
terminal = "alacritty"
changebrightnessup = "changebrightness up"
changebrightnessdown = "changebrightness down"
start_rofi = "rofi -show drun"
toggle_sink = "togglesink"


# Custom functions
def latest_group(qtile):
    qtile.current_screen.set_group(qtile.current_screen.previous_group)


# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == "monadtall":
        qtile.current_group.layout = "max"
    elif current_layout_name == "max":
        qtile.current_group.layout = "monadtall"

keys = [
    # Toggle fullscreen mod
    Key(
        [mod],
        "f",
        # maximize_by_switching_layout(),
        lazy.window.toggle_fullscreen(),
        desc="toggle fullscreen",
    ),

    # keybinding for monand tall layout
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "d", lazy.layout.shrink()),
    Key([mod], "r", lazy.layout.reset()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "grave", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [mod],
        "m",
        lazy.spawn(start_rofi),
        desc="Spawn a command using a prompt widget known as rofi",
    ),
    # change brightness with leisure keys
    Key(
        ["control", "shift"],
        "j",
        lazy.spawn(changebrightnessdown),
        desc="Change brightness down",
    ),
    Key(
        ["control", "shift"],
        "k",
        lazy.spawn(changebrightnessup),
        desc="Change brightness up",
    ),
    # Custom system bindings keybind
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("changebrightness up"),
        desc="Change brightness up",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("changebrightness down"),
        desc="Change brightness down",
    ),
    Key([], "XF86Tools", lazy.spawn(toggle_sink), desc="Change the default sink"),
    # color picker in X11
    Key([mod, "shift"], "c", lazy.spawn("xcolor -s clipboard")),
    # open thunar
    Key([], "XF86Explorer", lazy.spawn("thunar")),
    # go full black screen
    Key([], "XF86ScreenSaver", lazy.spawn("xset dpms force off")),
    # open rofi calculator
    Key([], "XF86Calculator", lazy.spawn("rofi -show calc")),
    # Screenshot
    Key([], "Print", lazy.spawn("screenshot")),
    Key(["shift"], "Print", lazy.spawn("screenshot select")),
    Key(["control"], "Print", lazy.spawn("screenshot window")),
    Key(["control", "shift"], "Print", lazy.spawn("screenshot sstoclipboard")),
    # Media keys
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    # Volume keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("changevolume up")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("changevolume down")),
    Key([], "XF86AudioMute", lazy.spawn("changevolume mute")),
    # Fix my shitty vacom tabet
    Key([mod, "shift"], "w", lazy.spawn("fixwacom")),
    # show power menu
    Key([mod, "shift"], "q", lazy.spawn("powermenu")),
    # get current power profile
    Key([mod, "shift"], "a", lazy.spawn("current_fan_boost.sh")),
    # Notifications
    Key([mod], "space", lazy.spawn("dunstctl close")),
    Key([mod, "shift"], "space", lazy.spawn("dunstctl close-all")),
    Key([mod, "shift"], "grave", lazy.spawn("dunstctl history-pop")),
    # Switching back and fourth between workspaces
    Key([mod], "tab", lazy.function(latest_group)),
    # Open figma
    Key([mod, "shift"], "f", lazy.spawn("firefox --new-window https://figma.com")),
    Key([], "XF86Search", lazy.spawn("firefox --new-window https://chat.openai.com")),
    # polybar toggle
    Key([mod, "shift"], "p", lazy.spawn("polybar-msg cmd toggle")),
    # open draw.io
    Key([mod, "shift"], "n", lazy.spawn("drawio")),
]

groups = [Group(i) for i in "1234567890"]
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

# Define scratchpads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "spotify", "spotify", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1
            ),
            DropDown(
                "firefox",
                "firefox --new-window https://youtube.com",
                width=0.8,
                height=0.8,
                x=0.1,
                y=0.1,
                opacity=1,
            ),
            DropDown(
                "volume",
                "alacritty --class=volume -e alsamixer",
                width=0.8,
                height=0.8,
                x=0.1,
                y=0.1,
                opacity=1,
            ),
            DropDown(
                "term2",
                "alacritty --class=scratch",
                width=0.8,
                height=0.8,
                x=0.1,
                y=0.1,
                opacity=1,
            ),
            DropDown(
                "timer", "gnome-clocks", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1
            ),
        ],
    )
)

# Scratchpad keybindings
keys.extend(
    [
        Key([mod], "s", lazy.group["scratchpad"].dropdown_toggle("spotify")),
        Key([mod], "v", lazy.group["scratchpad"].dropdown_toggle("volume")),
        Key([mod, "shift"], "t", lazy.group["scratchpad"].dropdown_toggle("term2")),
        Key([mod, "shift"], "m", lazy.group["scratchpad"].dropdown_toggle("firefox")),
        Key([], "XF86AudioStop", lazy.group["scratchpad"].dropdown_toggle("timer")),
    ]
)


layout_theme = {
    "border_width": 1,
    "margin": 10,
    "border_focus": "#26233a",
    "border_normal": "#1f1d2e",
}

full_screen_layout = {
    "border_width": 0,
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**full_screen_layout),
    # layout.Stack(num_stacks=2),
    # layout.Columns(**layout_theme),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def init_screens():
    return [
        Screen(top=bar.Gap(size=0)),
    ]


screens = init_screens()

# Drag floating layouts."
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button1", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = True
floats_kept_above = False
cursor_warp = False

floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        # ssh-askpass
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),  # gitk
        # GPG key password entry
        Match(title="pinentry"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


################ hooks ###################


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart")
    subprocess.Popen([home])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
