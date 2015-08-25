# -*- coding: utf-8 -*-

from DateTime import DateTime

from plone import api
from plone.app.layout.viewlets import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MessagesViewlet(ViewletBase):
    """This viewlet displays all messages from this product."""
    render = ViewPageTemplateFile('./messagesviewlet.pt')

    def getAllMessages(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        now = DateTime()
        brains = catalog.searchResults(portal_type=['Message'],
                                       start={'query': now, 'range': 'max'},
                                       end={'query': now, 'range': 'min'},
                                       sort_on='getObjPositionInParent')
        messages = []
        for brain in brains:
            messages.append(brain.getObject())

        return messages
