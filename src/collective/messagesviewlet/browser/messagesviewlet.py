# -*- coding: utf-8 -*-

from collective.messagesviewlet import HAS_PLONE_5_AND_MORE
from collective.messagesviewlet.utils import get_messages_to_show
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class MessagesViewletBase(common.ViewletBase):
    """This viewlet displays all messages from this product."""
    location_filter = []

    def is_plone_5(self):
        return HAS_PLONE_5_AND_MORE

    def getAllMessages(self):
        messages = get_messages_to_show(self.context)
        messages = [m for m in messages if m.location in self.location_filter]
        return messages

    def getCSSClassName(self, msg_type):
        mapping_type = {'info': 'info', 'significant': 'warning', 'warning': 'error'}
        return 'portalMessage {0}'.format(mapping_type[msg_type])

    def isLocalMessageAuthorized(self):
        registry = getUtility(IRegistry)
        return registry.get('messagesviewlet.authorize_local_message')

    def showMessage(self):
        return True


class GlobalMessagesViewlet(MessagesViewletBase):
    """Get global messages (homepage, messageconfig folder)"""
    id = "messagesviewlet"
    location_filter = ["fullsite", "homepage"]

    def showMessage(self):
        return True


class LocalMessagesViewlet(MessagesViewletBase):
    """Get local messages (From folderish)"""
    id = "localmessagesviewlet"
    location_filter = ["justhere", "fromhere"]

    def showMessage(self):
        registry = getUtility(IRegistry)
        return registry.get('messagesviewlet.show_local_message') and registry.get('messagesviewlet.authorize_local_message')
