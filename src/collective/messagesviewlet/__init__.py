# -*- coding: utf-8 -*-
"""Init and utils."""

from plone import api
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.messagesviewlet')

HAS_PLONE_5 = api.env.plone_version().startswith('5')
HAS_PAE = api.env.get_distribution('plone.app.event')
