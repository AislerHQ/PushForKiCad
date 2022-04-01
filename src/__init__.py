try:
    # On some Linux based systems site-packages are placed in a different directory.
    # KiCad only appends the system-wide directory to path,
    # because of this we add the user-wide directory, too.
    from sys import path
    import os
    path.append(os.path.expanduser('~/.local/lib/python3.9/site-packages'))
    
    from .plugin import PushForKiCadPlugin
    plugin = PushForKiCadPlugin()
    plugin.register()
except Exception as e:
    import logging
    root = logging.getLogger()
    root.debug(repr(e))
