# -*- coding: utf-8 -*-
from plone.dexterity.content import Container


class MessagesConfig(Container):
    """
        MessagesConfig class
    """

    # This method is used by index methods.
    # If None is returned, the linked content type is not catalogued
    def _getCatalogTool(self):
        return None
