# -*- coding: utf-8 -*-
from plone import api
from plone.indexer.wrapper import IndexableObjectWrapper

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
    logger.info('Import step dependency corrected')


def upgrade_to_2000(context):
    """
        Add timezone to start and end
    """
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='Message')
    logger.info('Found {0} messages'.format(len(brains)))
    count = 0
    for brain in brains:
        obj = brain.getObject()
        correction = False
        for attr in ('start', 'end'):
            if getattr(obj, attr, False):
                # use plone.indexer index to be sure we have same value
                indexable_wrapper = IndexableObjectWrapper(obj, catalog)
                setattr(obj, attr, getattr(indexable_wrapper, attr))
                correction = True
        if correction:
            count += 1
        # reindex entire object to avoid datetime with/without TZ comparison
        # that breaks metadata update
        obj.reindexObject()
    logger.info('Corrected {0} messages'.format(count))
