# -*- coding: utf-8 -*-
"""Init and utils."""

from plone import api
from zope.i18nmessageid import MessageFactory

import pkg_resources


_ = MessageFactory('collective.messagesviewlet')

HAS_PLONE_5_AND_MORE = api.env.plone_version().startswith('5') or api.env.plone_version().startswith('6')

try:
    api.env.get_distribution('plone.app.event')
    HAS_PAE = True
except pkg_resources.DistributionNotFound:
    HAS_PAE = False
