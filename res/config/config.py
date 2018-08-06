# Configuration
general = {
    'cmd_ident': '.',
    'def_channel_id': '',
}

modules = [
    'color_roles',
]

# Dictionaries of commands and associated module
cmd_mod = {
    'test':     'test',
    'help':     'help_command',
    'delete':   'delete',
    'color':    'set_color',
    'count-down':   'count_down',
}


# Dictionary of commands and according info
cmd_info = {
    'delete':   "`!delete last [number] [optional: user]` - Deletes the last "
                    "x(max=200) messages by anyone or an optional user.",
    'color':        "`!color [#hex-code]` - don't forget the #.",
    'count-down':   "`!count-down [ss/mm:ss/hh:mm:ss] [optional: event name]`"
}