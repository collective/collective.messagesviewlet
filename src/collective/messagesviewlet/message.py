# -*- coding: utf-8 -*-
from collective.messagesviewlet import _
from collective.messagesviewlet import HAS_PAE
from collective.messagesviewlet import HAS_PLONE_5_AND_MORE
from DateTime import DateTime
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.textfield import RichText
from plone.app.z3cform.widget import DatetimeFieldWidget as dtfw5
from plone.autoform import directives as form
from plone.indexer import indexer
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import six


if HAS_PAE:
    from plone.app.event.base import default_timezone
    from plone.app.event.base import localized_now

if not HAS_PLONE_5_AND_MORE:
    from plone.formwidget.datetime.z3cform.widget import DatetimeFieldWidget as dtfw4


def msg_types(context):
    terms = []
    terms.append(SimpleTerm("info", title=_("info")))
    terms.append(SimpleTerm("significant", title=_("significant")))
    terms.append(SimpleTerm("warning", title=_("warning")))
    return SimpleVocabulary(terms)


alsoProvides(msg_types, schema.interfaces.IContextSourceBinder)


def location(context):
    site = api.portal.getSite()
    config = site["messages-config"]
    terms = []
    terms.append(SimpleTerm("fullsite", title=_("Full site")))
    terms.append(SimpleTerm("homepage", title=_("Homepage")))
    terms.append(SimpleTerm("fromhere", title=_("From this content")))
    terms.append(SimpleTerm("justhere", title=_("Just on this content")))

    if IMessage.providedBy(context):
        # edit : context is the message.
        container = context.aq_parent
    else:
        # add : context is the folder (not yet the message).
        container = context
    if INavigationRoot.providedBy(container) or container == config:
        return SimpleVocabulary(terms[0:2])
    else:
        return SimpleVocabulary(terms[2:])


alsoProvides(location, schema.interfaces.IContextSourceBinder)


def generate_uid():
    return six.text_type(DateTime().millis())


def default_start():
    now = localized_now()
    return now.replace(minute=(now.minute - now.minute % 5), second=0, microsecond=0)


class IMessage(model.Schema):

    title = schema.TextLine(title=_(u"Title"), required=True,)

    text = RichText(title=_(u"Text"), required=True, description=_(u"Message text"),)

    msg_type = schema.Choice(
        title=_(u"Message type"),
        required=True,
        source=msg_types,
        description=_(u"Following the type, the color will be different"),
    )

    form.widget("can_hide", RadioFieldWidget)
    can_hide = schema.Bool(
        title=_(u"Can be marked as read"),
        description=_(u"If checked, the user can hide the message"),
        default=False,
    )

    start = schema.Datetime(
        title=_(u"Start date"),
        required=False,
        description=_(u"Specify start date message appearance"),
        defaultFactory=default_start,
    )
    if HAS_PLONE_5_AND_MORE:
        form.widget("start", dtfw5, default_timezone=default_timezone)
    else:
        form.widget("start", dtfw4)

    end = schema.Datetime(
        title=_(u"End date"),
        required=False,
        description=_(
            u"Specify end date message appearance. If nothing specified, this is infinite. "
            "If you pick a date, <span class=warning-formHelp>dont't forget hours !</span>"
        ),
    )
    if HAS_PLONE_5_AND_MORE:
        form.widget("end", dtfw5, default_timezone=default_timezone)
    else:
        form.widget("end", dtfw4)

    required_roles = schema.Set(
        title=_(u"Required roles"),
        description=_(u"Choose the roles for which the message will be displayed"),
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Roles"),
    )
    form.widget("required_roles", CheckBoxFieldWidget, multiple="multiple", size=15)

    form.widget("use_local_roles", RadioFieldWidget)
    use_local_roles = schema.Bool(
        title=_(u"Use Reader local role"),
        description=_(
            u"If checked, the message will be shown only to users having message local role 'Reader'"
        ),
        default=False,
    )

    location = schema.Choice(title=_(u"Location"), required=True, source=location,)

    hidden_uid = schema.TextLine(title=u"Generated uid", defaultFactory=generate_uid,)
    form.mode(hidden_uid="hidden")

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            data_start = add_timezone(data.start)
            data_end = add_timezone(data.end)
            if data_start > data_end:
                raise Invalid(_(u'The start date must precede the end date.'))


def add_timezone(dt, force=False):
    if HAS_PAE:
        TZ = default_timezone(as_tzinfo=True)
    if force or (not HAS_PLONE_5_AND_MORE and not dt.tzinfo):
        return TZ.localize(dt)
    return dt


@indexer(IMessage)
def start_index(obj):
    if obj.start is None:
        return obj.created()
    else:
        return add_timezone(obj.start)


@indexer(IMessage)
def end_index(obj):
    if obj.end is None:
        return DateTime('2099/01/01')
    else:
        return add_timezone(obj.end)


@implementer(IMessage)
class PseudoMessage(object):
    """
        This is not the class used with dexterity !
        This class is intended to be used in another context to instantiate messages that can be used in viewlet.
    """

    # Provide the minimal fields, needed in viewlet templates:
    msg_type = FieldProperty(IMessage["msg_type"])
    text = FieldProperty(IMessage["text"])
    can_hide = FieldProperty(IMessage["can_hide"])
    hidden_uid = FieldProperty(IMessage["hidden_uid"])

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
