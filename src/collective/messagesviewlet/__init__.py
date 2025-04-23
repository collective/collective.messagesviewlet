# -*- coding: utf-8 -*-
"""Init and utils."""

from importlib.metadata import version, PackageNotFoundError
from plone import api
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.messagesviewlet')

HAS_PLONE_5_AND_MORE = api.env.plone_version().startswith('5') or api.env.plone_version().startswith('6')

try:
    version('plone.app.event')
    HAS_PAE = True
except PackageNotFoundError:
    HAS_PAE = False
