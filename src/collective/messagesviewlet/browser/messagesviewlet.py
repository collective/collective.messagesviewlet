# -*- coding: utf-8 -*-

from collective.messagesviewlet import HAS_PLONE_5
from collective.messagesviewlet.utils import get_messages_to_show
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class MessagesViewlet(common.ViewletBase):
    """This viewlet displays all messages from this product."""

    def is_plone_5(self):
        return HAS_PLONE_5

    def getAllMessages(self):
        return get_messages_to_show(self.context)

    def getCSSClassName(self, msg_type):
        mapping_type = {'info': 'info', 'significant': 'warning', 'warning': 'error'}
        return 'portalMessage {0}'.format(mapping_type[msg_type])

    def isLocalMessageAuthorized(self):
        registry = getUtility(IRegistry)
        return registry.get('messagesviewlet.authorize_local_message')
