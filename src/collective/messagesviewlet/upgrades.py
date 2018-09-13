# -*- coding: utf-8 -*-
import logging
from plone import api
from plone.app.event.base import default_timezone

logger = logging.getLogger('collective.messagesviewlet: upgrade. ')


def upgrade_to_2000(context):
    """
        Add timezone to start and end
    """
    tzinfo = default_timezone(as_tzinfo=True)
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='Message')
    logger.info("Found %d messages" % len(brains))
    count = 0
    import ipdb; ipdb.set_trace()
    for brain in brains:
        obj = brain.getObject()
        correction = False
        for attr in ('start', 'end'):
            if getattr(obj, attr, False):
                setattr(obj, attr, tzinfo.localize(getattr(obj, attr)))
                correction = True
        if correction:
            count += 1
        obj.reindexObject(['start', 'end'])
    logger.info("Corrected %d messages" % count)
