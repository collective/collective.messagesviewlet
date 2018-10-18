# -*- coding: utf-8 -*-
import logging

from plone import api

logger = logging.getLogger('collective.messagesviewlet: upgrade. ')


def v1001(context):
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
