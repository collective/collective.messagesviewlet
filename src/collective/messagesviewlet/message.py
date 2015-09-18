# -*- coding: utf-8 -*-
from DateTime import DateTime
from datetime import datetime
from zope import schema
from zope.interface import invariant, Invalid, alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.formwidget.datetime.z3cform.widget import DatetimeFieldWidget
from plone.indexer import indexer
from plone.supermodel import model

from collective.messagesviewlet import _


def msg_types(context):
    terms = []
    terms.append(SimpleTerm("info", title=_("info")))
    terms.append(SimpleTerm("significant", title=_("significant")))
    terms.append(SimpleTerm("warning", title=_("warning")))
    return SimpleVocabulary(terms)

alsoProvides(msg_types, schema.interfaces.IContextSourceBinder)


def location(context):
    terms = []
    terms.append(SimpleTerm("fullsite", title=_("Full site")))
    terms.append(SimpleTerm("homepage", title=_("Homepage")))
    return SimpleVocabulary(terms)

alsoProvides(location, schema.interfaces.IContextSourceBinder)


def generate_uid():
    return unicode(DateTime().millis())


def default_start():
    return datetime.now()


class IMessage(model.Schema):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    text = RichText(
        title=_(u"Text"),
        required=True,
        description=_(u"Message text"),
    )

    msg_type = schema.Choice(
        title=_(u"Message type"),
        required=True,
        source=msg_types,
        description=_(u"Following the type, the color will be different"),
    )

    can_hide = schema.Bool(
        title=_(u"Can be marked as read"),
        description=_(u"If checked, the user can hide the message"),
    )

    start = schema.Datetime(
        title=_(u"Start date"),
        required=False,
        description=_(u"Specify start date message appearance"),
        defaultFactory=default_start,
    )
    form.widget('start', DatetimeFieldWidget)

    end = schema.Datetime(
        title=_(u"End date"),
        required=False,
        description=_(u"Specify end date message appearance. If nothing specified, this is infinite. "
                      "If you pick a date, <span class=warning-formHelp>dont't forget hours !</span>"),
    )
    form.widget('end', DatetimeFieldWidget)

    required_roles = schema.Set(
        title=_(u'Required roles'),
        description=_(u'Choose the roles for which the message will be displayed'),
        required=False,
        value_type=schema.Choice(vocabulary='plone.app.vocabularies.Roles'),
    )

    use_local_roles = schema.Bool(
        title=_(u"Use Reader local role"),
        description=_(u"If checked, the message will be shown only to users having message local role 'Reader'"),
        default=False,
    )

    location = schema.Choice(
        title=_(u"Location"),
        required=True,
        source=location,
    )

    hidden_uid = schema.TextLine(
        title=u"Generated uid",
        defaultFactory=generate_uid,
    )
    form.mode(hidden_uid='hidden')

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise Invalid(_(u"The start date must precede the end date."))


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
