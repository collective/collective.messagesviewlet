# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.base import default_timezone

import logging


logger = logging.getLogger('collective.messagesviewlet: upgrade. ')


def upgrade_to_1001(context):
    """ Avoid warning about unresolved dependencies """
    setup = api.portal.get_tool('portal_setup')
    registry = setup.getImportStepRegistry()
    config = {'collective-messagesviewlet-post-install': (u'browserlayer', u'controlpanel', u'cssregistry',
                                                          u'propertiestool', u'rolemap', u'typeinfo', u'workflow'),
              'collective-messagesviewlet-messages': ()}
    for key, value in config.items():
        step = registry._registered.get(key)
        if step is not None:
            step['dependencies'] = value
    setup._p_changed = True
    logger.info("Import step dependency corrected")


def upgrade_to_2000(context):
    """
        Add timezone to start and end
    """
    tzinfo = default_timezone(as_tzinfo=True)
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='Message')
    logger.info("Found %d messages" % len(brains))
    count = 0
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
