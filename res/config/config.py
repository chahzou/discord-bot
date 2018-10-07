# Configuration
general = {
    'cmd_op': '!',
    'name': "",
    'def_channel_id': '',
}


# Modules that should be available
modules = [
    'Info',
    'Help',
    'Test',
    'Administration',
    'Registration',
    'ColorRoles',
]

# Other
other = {
    'ready_msg_toggle': True,
    'ready_msg': "Now online.",
    'leave_msg': " left the server.",    # Preceded by the user who left the server.
    'max_msg_len': 10000,
    'max_args': 100,
    'auto_delete_msgs_channel_ids': [''],
    'auto_delete_delay_s': 10,
    'clear_channel_ids': [''],
}