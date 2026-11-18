from collective.messagesviewlet import _
from plone.app.registry.browser import controlpanel
from plone.z3cform import layout
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from zope import schema
from zope.component.hooks import getSite
from zope.interface import Interface


class IMessagesviewletSettings(Interface):

    authorize_local_message = schema.Bool(
        title=_("Authorize local messages"),
        description=_(
            "Check if messages can be added everywhere on the site. This also affects visibility of existing local messages."
        ),
        required=False,
        default=False,
    )

    show_local_message = schema.Bool(
        title=_("Show local messages"),
        description=_(
            "Affects only messages visibility. Check if you want to see local messages."
        ),
        required=False,
        default=False,
    )


class MessagesviewletControlPanelForm(controlpanel.RegistryEditForm):
    schema = IMessagesviewletSettings
    schema_prefix = "messagesviewlet"
    label = _("Messages viewlet settings")

    @button.buttonAndHandler(_("Save"), name="save")
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
        IStatusMessage(self.request).addStatusMessage(("Changes saved."), "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."), "info")
        self.request.response.redirect(
            f"{getSite().absolute_url()}/{self.control_panel_view}"
        )


class MessagesviewletControlPanelFormWrapper(controlpanel.ControlPanelFormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """

    index = ViewPageTemplateFile("templates/controlpanel_layout.pt")


MessagesviewletControlPanelView = layout.wrap_form(
    MessagesviewletControlPanelForm, MessagesviewletControlPanelFormWrapper
)
