# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface, alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.messagesviewlet import _
from plone.app.textfield import RichText


def msg_types(context):
    terms = []
    terms.append(SimpleTerm("info", title=_("Info")))
    terms.append(SimpleTerm("warning", title=_("Warning")))
    terms.append(SimpleTerm("important", title=_("Important")))
    return SimpleVocabulary(terms)

alsoProvides(msg_types, schema.interfaces.IContextSourceBinder)


def location(context):
    terms = []
    terms.append(SimpleTerm("fullsite", title=_("Full site")))
    terms.append(SimpleTerm("homepage", title=_("Homepage")))
    return SimpleVocabulary(terms)

alsoProvides(location, schema.interfaces.IContextSourceBinder)


class IMessage(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    text = RichText(
        title=_("Text"),
        required=True,
    )

    msg_type = schema.Choice(
        title=_(u"Message type"),
        required=True,
        source=msg_types,
    )

    location = schema.Choice(
        title=_(u"Location"),
        required=True,
        source=location,
    )

    start = schema.Datetime(
        title=_(u"Start date"),
        required=False,
    )

    end = schema.Datetime(
        title=_(u"End date"),
        required=False,
    )
