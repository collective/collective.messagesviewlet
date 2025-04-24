# -*- coding: utf-8 -*-
"""Init and utils."""

from plone import api
from zope.i18nmessageid import MessageFactory

import six

if six.PY2:
    from pkg_resources import DistributionNotFound as PackageNotFoundError
else:
    from importlib.metadata import version, PackageNotFoundError


_ = MessageFactory('collective.messagesviewlet')

HAS_PLONE_5_AND_MORE = api.env.plone_version().startswith('5') or api.env.plone_version().startswith('6')

try:
    if six.PY2:
        api.env.get_distribution('plone.app.event')
    else:
        version('plone.app.event')
    HAS_PAE = True
except PackageNotFoundError:
    HAS_PAE = False
