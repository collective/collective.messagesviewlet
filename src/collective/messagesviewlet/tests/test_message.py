# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.messagesviewlet.testing import COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING  # noqa
from collective.messagesviewlet.message import IMessage

import unittest2 as unittest


class MessageIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Message')
        schema = fti.lookupSchema()
        self.assertEqual(IMessage, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Message')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Message')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IMessage.providedBy(obj))

    def test_adding(self):
        folder = getattr(self.portal, "messages-config", None)
        folder.invokeFactory('Message', 'Message')
        self.assertTrue(
            IMessage.providedBy(folder['Message'])
        )
