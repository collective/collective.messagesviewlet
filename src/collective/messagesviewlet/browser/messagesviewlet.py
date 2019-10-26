# -*- coding: utf-8 -*-

from collective.messagesviewlet import HAS_PLONE_5
from collective.messagesviewlet.utils import get_messages_to_show
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MessagesViewlet(ViewletBase):
    """This viewlet displays all messages from this product."""
    render = ViewPageTemplateFile('./messagesviewlet.pt')

    def is_plone_5(self):
        return HAS_PLONE_5

    def getAllMessages(self):
        return get_messages_to_show(self.context)

    def getCSSClassName(self, msg_type):
        mapping_type = {'info': 'info', 'significant': 'warning', 'warning': 'error'}
        return 'portalMessage {0}'.format(mapping_type[msg_type])
