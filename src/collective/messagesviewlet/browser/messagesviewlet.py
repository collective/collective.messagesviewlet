# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.messagesviewlet.message import IMessage

from plone import api
from plone.app.layout.viewlets import ViewletBase


class MessagesViewlet(ViewletBase):
    """This viewlet displays all messages from this product."""
    render = ViewPageTemplateFile('./messagesviewlet.pt')

    def available(self):
        return len(self.getAllMessages()) > 0

    def getAllMessages(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.unrestrictedSearchResults(object_provides=IMessage.__identifier__)
        messages = [brain.getObject() for brain in brains]

        return messages
