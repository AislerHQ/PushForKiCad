try:
    from .plugin import PushForKiCadPlugin
    plugin = PushForKiCadPlugin()
    plugin.register()
except Exception as e:
    import logging    
    root = logging.getLogger()
    root.debug(repr(e))