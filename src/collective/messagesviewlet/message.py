# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface

from collective.messagesviewlet import _


class IMessage(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
