# -*- coding: utf-8 -*-

from DateTime import DateTime

from plone import api
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.behavior.talcondition.utils import evaluateExpressionFor


class MessagesViewlet(ViewletBase):
    """This viewlet displays all messages from this product."""
    render = ViewPageTemplateFile('./messagesviewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(MessagesViewlet, self).__init__(context, request, view, manager=manager)
        self.portal = api.portal.get()

    def getAllMessages(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        # Getting user roles on context
        if api.user.is_anonymous():
            mb_roles = set(['Anonymous'])
        else:
            mb_roles = set(api.user.get_roles(obj=self.context))
        now = DateTime()
        brains = catalog.unrestrictedSearchResults(portal_type=['Message'],
                                                   start={'query': now, 'range': 'max'},
                                                   end={'query': now, 'range': 'min'},
                                                   review_state=('activated'),
                                                   sort_on='getObjPositionInParent')
        messages = []
        for brain in brains:
            if brain.location == 'homepage':
                # Test if context is PloneSite or its default page
                if not INavigationRoot.providedBy(self.context) and \
                        not isDefaultPage(self.portal, self.context):
                    continue
            obj = brain._unrestrictedGetObject()
            # check in the cookie if message is marked as read
            if obj.can_hide:
                m_uids = self.request.get('messagesviewlet', '')
                if obj.hidden_uid in m_uids.split('|'):
                    continue
            # check if member has a required role on the context
            if obj.required_roles:
                if mb_roles.intersection(obj.required_roles) == set():
                    continue
            # We define obj.context to viewlet context to evaluate expression on viewlet context display.
            if not evaluateExpressionFor(obj, extra_expr_ctx={'context': self.context}):
                continue
            # We check the local roles
            if obj.use_local_roles and not api.user.is_anonymous() and 'Reader' not in api.user.get_roles(obj=obj):
                continue
            messages.append(obj)

        return messages
