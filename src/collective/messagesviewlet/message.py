# -*- coding: utf-8 -*-
from DateTime import DateTime
from zope import schema
from zope.interface import Interface, alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.messagesviewlet import _
from plone.app.textfield import RichText
from plone.indexer import indexer


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
        title=_(u"Text"),
        required=True,
        description=_(u"Alert message"),
    )

    msg_type = schema.Choice(
        title=_(u"Message type"),
        required=True,
        source=msg_types,
        description=_(u"Alert type"),
    )

    location = schema.Choice(
        title=_(u"Location"),
        required=True,
        source=location,
    )

    start = schema.Datetime(
        title=_(u"Start date"),
        required=False,
        description=_(u"Specify start date message appearance"),
    )

    end = schema.Datetime(
        title=_(u"End date"),
        required=False,
        description=_(u"Specify end date message appearance"),
    )


@indexer(IMessage)
def start_index(obj):
    if obj.start is None:
        return obj.created()
    else:
        return obj.start


@indexer(IMessage)
def end_index(obj):
    if obj.end is None:
        return DateTime(2099, 01, 01)
    else:
        return obj.end
