# Configuration
general = {
    'cmd_op': '!',
    'def_channel_id': '',
}

modules = [
    'color_roles',
]

# Dictionaries of commands and associated module
arg_mod_assoc = {
    'info':     'info',
    'help':     'help',
    'test':     'test',
    'color':    'color',
}


# Dictionary of commands and according info
cmd_info = {
    'delete':   "`!delete last [number] [optional: user]` - Deletes the last "
                    "x(max=200) messages by anyone or an optional user.",
    'color':        "`!color [#hex-code]` - don't forget the #.",
    'count-down':   "`!count-down [ss/mm:ss/hh:mm:ss] [optional: event name]`"
}