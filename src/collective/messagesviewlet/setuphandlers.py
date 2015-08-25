# -*- coding: utf-8 -*-


def post_install(context):
    """Post install script."""
    if context.readDataFile('collectivemessagesviewlet_default.txt') is None:
        return
