# -*- coding: utf-8 -*-
from datetime import datetime
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from plone import api
from plone.app.textfield.value import RichTextValue
from message import generate_uid


def _(msgid, context, domain='collective.messagesviewlet'):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, context=context.REQUEST)


def _richtextval(text):
    """ Return a RichTextValue """
    if not isinstance(text, unicode):
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
    site = api.portal.getSite()
    config = site['messages-config']
    # We pass if id already exists
    if id in config:
        return None
    rich_text = _richtextval(text)
    try:
        end_date = datetime.strptime(end, '%Y%m%d-%H%M')
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
