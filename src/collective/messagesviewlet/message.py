# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface

from collective.messagesviewlet import _
from plone.app.textfield import RichText


class IMessage(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    message = RichText(
        title=_("Text"),
        required=True,
    )

    start = schema.Datetime(
        title=_(u"Start date"),
        required=False,
    )

    end = schema.Datetime(
        title=_(u"End date"),
        required=False,
    )

    msg_type = schema.Choice(
        title=_(u"Message type"),
        required=True,
        values=[_(u'Info'), _(u'Warning'), _(u'Important')]
    )

    location = schema.Choice(
        title=_(u"Location"),
        required=True,
        values=[_(u'Full Site'), _(u'Homepage')]
    )
