# -*- coding: utf-8 -*-
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

from zope.component import queryUtility
from zope.component import createObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
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

    def _createMessage(self, title, text, msg_type="info", location="fullsite", can_hide=True,
                       start_date=DateTime() - 1, end_date=DateTime() + 1,
                       tal_condition="python:True", roles_bypassing_talcondition=[]):
        """Method to create one message"""
        message = api.content.create(
            type="Message",
            title=title,
            text=RichTextValue(raw=text, mimeType='text/html', outputMimeType='text/html', encoding='utf-8'),
            msg_type=msg_type,
            location=location,
            can_hide=can_hide,
            start=start_date,
            end=end_date,
            container=self.message_config_folder,
        )
        ITALCondition(message).tal_condition = tal_condition
        ITALCondition(message).roles_bypassing_talcondition = roles_bypassing_talcondition
        self.messages.append(message)

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        membershopTool = getToolByName(self.portal, 'portal_membership')
        self.member = membershopTool.getAuthenticatedMember()
        self.portal.REQUEST['AUTHENTICATED_USER'] = self.member

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.message_types = ["info", "significant", "warning"]
        self.isHidden = [True, True, False]
        self.portal = self.layer['portal']
        # The products build the "special" folder "messages-config" to store messages.
        self.message_config_folder = getattr(self.portal, "messages-config", None)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.messages = []
        # Create some messages
        for i, message_type in enumerate(self.message_types):
            title = 'message%d' % (i + 1)
            text = "<p>This is test message number %d...</p>"\
                   "<p>self-destruction programmed at the end of this test.</p>" % (i + 1)
            self._createMessage(title=title,
                                text=text,
                                msg_type=self.message_types[i],
                                can_hide=self.isHidden[i])

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
        for i, message_type in enumerate(self.message_types):
            message = 'message%d' % (i + 1)
            self.assertTrue(IMessage.providedBy(self.message_config_folder[message]))

    def test_getAllMessages_wf(self):
        """
        """
        viewlet = MessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        # no message in viewlet because all messages are in "inactive" state
        self.assertEqual(len(viewlet.getAllMessages()), 0)
        wftool = self.portal.portal_workflow
        # activate for anonymous the first message
        wftool.doActionFor(self.messages[0], 'activate_for_anonymous')
        # viewlet contain one message
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0], )))
        # activate for members the second message
        wftool.doActionFor(self.messages[1], 'activate_for_members')
        # viewlet contain one message
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0], self.messages[1])))
        # activate for local roles the third message
        wftool.doActionFor(self.messages[2], 'activate_for_local_roles')
        # viewlet contain one message
        self.assertEqual(len(viewlet.getAllMessages()), 3)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0], self.messages[1], self.messages[2])))
        # return to anonymous fe... only one message should be visible.
        logout()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0], )))

    def test_getAllMessages(self):
        """
        """
        viewlet = MessagesViewlet(self.message_config_folder, self.message_config_folder.REQUEST, None, None)
        viewlet.update()
        wftool = self.portal.portal_workflow
        # activate all messages.
        for i, message_type in enumerate(self.message_types):
            wftool.doActionFor(self.messages[i], 'activate_for_anonymous')
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types))
        # Please keep chronological methods.
        self._getAllMessages_test_date(viewlet)
        self._getAllMessages_test_tal_condition(viewlet)
        self._getAllMessages_test_location(viewlet)

    def _getAllMessages_test_date(self, viewlet):
        # set message as message 0 and change date to ignore it.
        message = self.messages[0]
        message.start = DateTime() + 1
        # reindex object for catalog...
        message.reindexObject()
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        # test if printed messages are 1 and 2 without message 0
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[1], self.messages[2])))
        message = self.messages[1]
        message.end = DateTime() - 2
        # reindex object for catalog...
        message.reindexObject()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        # test if printed message is 2 without messages 0 and 1
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[2], )))

        # tests if message with date set to None is still available
        message = self.messages[2]
        message.start = message.end = None
        # reindex object for catalog...
        message.reindexObject()
        # tests that the message is still visible.
        self.assertEqual(len(viewlet.getAllMessages()), 1)

    def _getAllMessages_test_tal_condition(self, viewlet):
        message = self.messages[2]
        message.tal_condition = "python:False"
        self.assertEqual(len(viewlet.getAllMessages()), 0)

    def _getAllMessages_test_location(self, viewlet):
        message = self.messages[2]
        message.tal_condition = "python:True"
        message.location = "homepage"
        message.reindexObject()
        self.assertEqual(len(viewlet.getAllMessages()), 0)

    def test_viewlet_rendering(self):
        """
        Test if viewlet rendering is ok (text and css class)
        """
        viewlet = MessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        wftool = self.portal.portal_workflow
        # activate one message.
        wftool.doActionFor(self.messages[0], 'activate_for_anonymous')
        # viewlet.render()
        viewlet_rendering = viewlet.context()
        self.assertIn(self.messages[0].text.output, viewlet_rendering)
        self.assertIn('messagesviewlet-info', viewlet_rendering)
        self.assertNotIn(self.messages[1].text.output, viewlet_rendering)
        self.assertNotIn(self.messages[2].text.output, viewlet_rendering)

    def test_hidden_uid_when_workflow_changes(self):
        wftool = self.portal.portal_workflow
        # saves the hidden uid before it changes because of the workflow
        # modifications
        hidden_uid = self.messages[0].hidden_uid
        wftool.doActionFor(self.messages[0], 'activate_for_anonymous')
        wftool.doActionFor(self.messages[0], 'disactivate')
        # checks if the hidden uid has whell changed.
        self.assertNotEqual(hidden_uid, self.messages[0])

    def test_required_roles_permissions(self):
        wftool = self.portal.portal_workflow
        for i, message_type in enumerate(self.message_types):
            wftool.doActionFor(self.messages[i], 'activate_for_anonymous')
        viewlet = MessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        # Sets the required role to 'Authenticated' to message 1
        self.messages[0].required_roles = set(['Authenticated'])
        # Checks that we still see all messages as we are authenticated
        self.assertEqual(len(viewlet.getAllMessages()), 3)
        logout()
        # Checks that an anonymous user can't see anymore the restricted one.
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[1], self.messages[2])))
