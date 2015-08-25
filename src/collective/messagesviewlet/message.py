# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from zope.i18n import translate
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.messagesviewlet import _
from plone.app.textfield import RichText


def msg_type(context):
    terms = []
    terms.append(SimpleTerm("info", title=translate("Info", domain="collective.messagesviewlet",
                            context=context.REQUEST)))
    terms.append(SimpleTerm("warning", title=translate("Warning", domain="collective.messagesviewlet",
                            context=context.REQUEST)))
    terms.append(SimpleTerm("important", title=translate("Important", domain="collective.messagesviewlet",
                            context=context.REQUEST)))
    return SimpleVocabulary(terms)


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
        source=msg_type
    )

    location = schema.Choice(
        title=_(u"Location"),
        required=True,
        values=[_(u'Full Site'), _(u'Homepage')]
    )
