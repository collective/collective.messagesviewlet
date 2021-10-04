# -*- coding: utf-8 -*-

from collective.messagesviewlet import _
from plone.app.registry.browser import controlpanel
from plone.z3cform import layout
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from zope import schema
from zope.component.hooks import getSite
from zope.interface import Interface


class IMessagesviewletSettings(Interface):

    authorize_local_message = schema.Bool(
        title=_(u"Authorize local message"),
        description=_(
            u"Check if message can be globally allow (Can haven't influence if Message is explicitly authorised on container). Also affecting visibility."
        ),
        required=False,
        default=False,
    )

    show_local_message = schema.Bool(
        title=_(u"Show local message"),
        description=_(
            u"Affecting only visibility. Check if you want to see local messages."
        ),
        required=False,
        default=False,
    )


class MessagesviewletControlPanelForm(controlpanel.RegistryEditForm):
    schema = IMessagesviewletSettings
    schema_prefix = "messagesviewlet"
    label = _(u"Messagesviewlet Settings")

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleSave(self, action):
        data, errors = self.extractData()
        portal_types = self.context.portal_types
        lpf = portal_types["Message"]
        if data.get("authorize_local_message") is True:
            lpf.global_allow = True
        else:
            lpf.global_allow = False
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage((u"Changes saved."), "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_(u"Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes canceled."), "info")
        self.request.response.redirect(
            u"{0}/{1}".format(getSite().absolute_url(), self.control_panel_view)
        )


class MessagesviewletControlPanelFormWrapper(controlpanel.ControlPanelFormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """

    index = ViewPageTemplateFile("templates/controlpanel_layout.pt")

    def get_portal_url(self):
        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject()
        portalPath = portal.getPhysicalPath()
        return "/".join(portalPath)


MessagesviewletControlPanelView = layout.wrap_form(
    MessagesviewletControlPanelForm, MessagesviewletControlPanelFormWrapper
)
