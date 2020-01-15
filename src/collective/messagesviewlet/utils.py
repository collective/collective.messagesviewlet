# -*- coding: utf-8 -*-

from collective.behavior.talcondition.behavior import ITALCondition
from collective.messagesviewlet import HAS_PLONE_5
from collective.messagesviewlet.message import add_timezone
from collective.messagesviewlet.message import generate_uid
from datetime import datetime
from DateTime import DateTime
from plone import api
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.textfield.value import RichTextValue
from six import text_type
from zope.annotation import IAnnotations
from zope.component import queryUtility
from zope.globalrequest import getRequest
from zope.i18n.interfaces import ITranslationDomain


def _(msgid, context, domain='collective.messagesviewlet', mapping=None):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, context=context.REQUEST, mapping=mapping)


def _richtextval(text):
    """ Return a RichTextValue """
    if not isinstance(text, text_type):
        text = text.decode('utf8')
    return RichTextValue(raw=text, mimeType='text/html', outputMimeType='text/html', encoding='utf-8')


def add_message(id, title, text, msg_type='info', can_hide=False, start=datetime.now(), end='', req_roles=[],
                location='fullsite', tal_condition='', roles_byp_talcond=[], use_local_roles=False, activate=False):
    """
        Add a message in the configuration folder
            msg_type: info, significant, warning
            start: default now
            end: default empty, or use pattern YYYYMMDD-HHSS
            location: fullsite, homepage
    """
    site = api.portal.get()
    config = site['messages-config']
    # We pass if id already exists
    if id in config:
        return None
    rich_text = _richtextval(text)
    # Add TZ when using Plone5
    if HAS_PLONE_5:
        start = add_timezone(start, force=True)
    try:
        end_date = datetime.strptime(end, '%Y%m%d-%H%M')
        end_date = add_timezone(end_date, force=True)
    except ValueError:
        end_date = None
    message = api.content.create(container=config, type='Message', id=id, title=title,
                                 **{'msg_type': msg_type, 'text': rich_text, 'can_hide': can_hide,
                                    'start': start, 'end': end_date, 'required_roles': req_roles,
                                    'location': location, 'hidden_uid': generate_uid(),
                                    'tal_condition': tal_condition, 'roles_bypassing_talcondition': roles_byp_talcond,
                                    'use_local_roles': use_local_roles})
    if activate:
        api.content.transition(message, 'activate')
    return message


def get_messages_to_show(context, caching=True):
    """
        Returns every message to be displayed for current context.
    """
    messages = None
    if caching:
        request = getRequest()
        if request:
            key = 'messagesviewlet-utils-get_messages_to_show-{0}'.format(
                '_'.join(context.getPhysicalPath()))
            cache = IAnnotations(request)
            messages = cache.get(key, None)
        else:
            caching = False

    if messages is None:
        messages = []
        portal = api.portal.get()
        catalog = api.portal.get_tool(name='portal_catalog')
        # Getting user roles on context
        if api.user.is_anonymous():
            mb_roles = set(['Anonymous'])
        else:
            mb_roles = set(api.user.get_roles(obj=context))
        now = DateTime()
        brains = catalog.unrestrictedSearchResults(portal_type=['Message'],
                                                   start={'query': now, 'range': 'max'},
                                                   end={'query': now, 'range': 'min'},
                                                   review_state=('activated'),
                                                   sort_on='getObjPositionInParent')
        for brain in brains:
            message = brain._unrestrictedGetObject()
            if message.location == 'homepage':
                # Test if context is PloneSite or its default page
                if not INavigationRoot.providedBy(context) and \
                        not isDefaultPage(portal, context):
                    continue
            # check in the cookie if message is marked as read
            if message.can_hide:
                m_uids = context.REQUEST.get('messagesviewlet', '')
                if message.hidden_uid in m_uids.split('|'):
                    continue
            # check if member has a required role on the context
            if message.required_roles:
                if mb_roles.intersection(message.required_roles) == set():
                    continue
            # We define obj.context to viewlet context to evaluate expression on viewlet context display.
            if not ITALCondition(message).evaluate(extra_expr_ctx={'context': context}):
                continue
            # We check the local roles
            if message.use_local_roles and \
               not api.user.is_anonymous() and \
               'Reader' not in api.user.get_roles(obj=message):
                continue
            messages.append(message)

        if caching:
            cache[key] = messages

    return messages
