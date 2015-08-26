# -*- coding: utf-8 -*-
from DateTime import DateTime

from zope.component import queryUtility
from zope.component import createObject

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.behavior.talcondition.behavior import ITALCondition
from collective.messagesviewlet.browser.messagesviewlet import MessagesViewlet
from collective.messagesviewlet.message import IMessage
from collective.messagesviewlet.testing import COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING  # noqa

import unittest2 as unittest


class MessageIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.message_config_folder = getattr(self.portal, "messages-config", None)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        # Message creation.
        text = "<p>This is a new test message...</p>"\
               "<p>self-destruction programming at the end of this test.</p>"
        msg_type = "warning"
        location = "fullsite"
        start_date = DateTime() - 1
        end_date = DateTime() + 1
        self.message = api.content.create(
            type="Message",
            title="Test message",
            text=text,
            msg_type=msg_type,
            location=location,
            start=start_date,
            end=end_date,
            container=self.message_config_folder,
        )
        ITALCondition(self.message).tal_condition = "python:True"
        ITALCondition(self.message).roles_bypassing_talcondition = []

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
        # The products build the "special" folder "messages-config" to store messages.
        self.message_config_folder.invokeFactory('message', 'Message')
        self.assertTrue(
            IMessage.providedBy(self.message_config_folder['message'])
        )

    def test_rendering(self):
        """
        """
        viewlet = MessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        import ipdb;ipdb.set_trace()
