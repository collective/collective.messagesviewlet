# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from DateTime import DateTime

from plone import api
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.layout.viewlets import ViewletBase
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
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
            if brain.location == 'homepage':
                if not IPloneSiteRoot.providedBy(self.context) and \
                        not isDefaultPage(aq_parent(self.context), self.context):
                    continue
            messages.append(brain.getObject())

        return messages
