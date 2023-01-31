import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from libqtile import layout, bar, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile.widget import Spacer
#import arcobattery

#mod4 or mod = super key1
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

# Fonts 
font2 = 'CaskaydiaCove Nerd Font'
font1 = "FiraCode Nerd Font"
font2 = "Font awesome"

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "Return", lazy.spawn('alacritty')),
    Key([mod], "b", lazy.spawn('brave')),

# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "t", lazy.next_layout()),
    Key([mod], "space", lazy.widget['keyboardlayout'].next_keyboard(),desc='Next keyboard layout'),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

#group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
group_labels = ["", "", "", "", "", "", "", "", "", "ﬁ"]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "control"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

# Add a ScratchPad Group With a terminal dropdown
groups.append(
    ScratchPad("scratchpad", [
        DropDown("term", "alacritty", y=0.15,height=0.7),
        DropDown("python", "alacritty -e 'python' ", y=0.15,height=0.7)
        ])
    )
# Add ScratchPad toogle key
keys.extend([
    Key([mod, "shift"], "Return", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod, "shift"], "p", lazy.group['scratchpad'].dropdown_toggle('python')),
])

def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#46D9FF",
            "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(margin=15, border_width=1, border_focus="#46D9FF", border_normal="#00000000"),
    layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]
# COLORS FOR THE BAR
#Theme name : ArcoLinux Default
def init_colors():
    return [["#282c34", "#282c34"], # color 0  
            ["#9ca0a4", "#979797"], # color 1  
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#DFDFDF", "#dfdfdf"], # color 3 
            ["#fcd71c", "#fcd71c"], # color 4  
            ["#ff6c6b", "#ff6655"], # color 5
            ["#da8548", "#dd8844"], # color 6
            ["#98be65", "#99bb66"], # color 7
            ["#4db5bd", "#44b9b1"], # color 8
            ["#46D9FF", "#46D9FF"], # color 9
            ["#51afef", "#51afef"], # color 10
            ["#2257A0", "#2257A0"], # color 11
            ["#c678dd", "#c678dd"], # color 12
            ["#a9a1e1", "#a9a1e1"]] # color 13


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2)

widget_defaults = init_widgets_defaults()

cust_spacer = widget.Spacer(length=5)

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
                widget.Image(
                        font=font1,
                        filename='~/.config/qtile/icons/python.png',
                        padding=0,
                        fontsize=16,
                        mouse_callbacks={'Button1': lazy.spawn('alacritty')},
                        decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]
                ),
                cust_spacer,
                widget.Clock(
                        font=font1,
                        format="    %d/%m/%y  %H:%M  ",
                        foreground=colors[3],
                        padding=0,
                        fontsize=16,
                        decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]

                ),
                cust_spacer,
                widget.Net(
                        font=font1,
                        foreground=colors[10],
                        padding=0,
                        format='   {down} {up}  ',
                        fontsize=16,
                        prefix='M',
                         decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]
                ),
                cust_spacer,
                widget.Backlight(
                        font=font1,
                        backlight_name='intel_backlight',
                        foreground=colors[4],
                        padding=0,
                        format='  {percent:2.0%} ',
                        fontsize=16,
                         decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]
                ),
                widget.Spacer(
                        length=210,
                ),
                widget.GroupBox(font=font1,
                        fontsize = 15,
                        margin_y = 2,
                        margin_x = 10,
                        padding_y = 0,
                        padding_x = 8,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[9],
                        inactive = colors[3],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[12],
                        foreground = colors[3],
                        decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]
                        ),
                widget.Spacer(
                        length=200,
                ),
                cust_spacer,
                widget.Battery(
                    font=font1,
                    foreground=colors[7],
                    padding=0,
                    show_short_text=False,
                    full_char='󰁹',
                    charge_char='',
                    discharge_char='',
                    empty_char='',
                    format='  {char} {percent:2.0%}  ',
                    fontsize=16,
                    update_interval=1,
                        decorations=[
                        RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                    ]
                ),
                cust_spacer,
                widget.KeyboardLayout(
                        font=font1,
                        configured_keyboards=['es','us'],
                        foreground=colors[5],
                        padding=0,
                        fmt='    {}  ',
                        fontsize=16,
                        decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]
                ),
                cust_spacer,
                widget.CPU(
                        font=font1,
                        foreground=colors[12],
                        padding=0,
                        format='   {load_percent}%  ',
                        fontsize=16,
                        update_interval=1,
                         decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]
                ),
                cust_spacer,
                widget.Memory(
                        font=font1,
                        foreground=colors[4],
                        padding=0,
                        format='   {MemUsed: .1f}{mm}/{MemTotal: .1f}{mm}  ',
                        fontsize=16,
                        measure_mem='G',
                        decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]
                ),
                cust_spacer,
                widget.Volume(
                        font=font1,
                        foreground=colors[8],
                        padding=0,
                        fmt='  墳 {}  ',
                        fontsize=16,
                        scroll=True,
                         decorations=[
                            RectDecoration(colour=colors[0], radius=13, filled=True, padding_y=0)
                        ]

                ),
                cust_spacer                        
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, background="#00000000",border_width=5,border_color="#00000000"))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules, 
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
