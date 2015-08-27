# -*- coding: utf-8 -*-
from DateTime import DateTime

from zope.component import queryUtility
from zope.component import createObject

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.behavior.talcondition.behavior import ITALCondition
from collective.messagesviewlet.browser.messagesviewlet import MessagesViewlet
from collective.messagesviewlet.message import IMessage
from collective.messagesviewlet.testing import COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING  # noqa

import unittest2 as unittest


class MessageIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def _createMessage(self, title, text, msg_type="info", location="fullsite", start_date=DateTime() - 1,
                       end_date=DateTime() + 1, tal_condition="python:True", roles_bypassing_talcondition=[]):
        """Method to create one message"""
        message = api.content.create(
            type="Message",
            title=title,
            text=RichTextValue(raw=text, mimeType='text/html', outputMimeType='text/html', encoding='utf-8'),
            msg_type=msg_type,
            location=location,
            start=start_date,
            end=end_date,
            container=self.message_config_folder,
        )
        ITALCondition(message).tal_condition = tal_condition
        ITALCondition(message).roles_bypassing_talcondition = roles_bypassing_talcondition
        self.messages.append(message)

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.message_config_folder = getattr(self.portal, "messages-config", None)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.messages = []
        # Create some messages
        for i in range(1, 5):
            title = 'message%d' % i
            text = "<p>This is test message number %d...</p>"\
                   "<p>self-destruction programming at the end of this test.</p>" % i
            self._createMessage(title, text)

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
        for i in range(1, 5):
            message = 'message%d' % i
            self.assertTrue(IMessage.providedBy(self.message_config_folder[message]))

    def test_rendering(self):
        """
        """
        viewlet = MessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        # no message in viewlet because all messages are in "inactive" state
        self.assertEqual(len(viewlet.getAllMessages()), 0)
        wftool = self.portal.portal_workflow
        #activate for anonymous the first message
        wftool.doActionFor(self.messages[0], 'activate_for_anonymous')
        # viewlet contain one message
        self.assertEqual(len(viewlet.getAllMessages()), 1)
