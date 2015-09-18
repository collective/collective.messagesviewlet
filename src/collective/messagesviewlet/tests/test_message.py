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
        membershipTool = getToolByName(self.portal, 'portal_membership')
        self.member = membershipTool.getAuthenticatedMember()
        self.portal.REQUEST['AUTHENTICATED_USER'] = self.member

    def _set_viewlet(self):
        """
        """
        viewlet = MessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        # activate all messages.
        for i, message_type in enumerate(self.message_types):
            self.wftool.doActionFor(self.messages[i], 'activate')
        return viewlet

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.message_types = ["info", "significant", "warning"]
        self.isHidden = [True, True, False]
        self.portal = self.layer['portal']
        # The products build the "special" folder "messages-config" to store messages.
        self.message_config_folder = self.portal["messages-config"]
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.wftool = self.portal.portal_workflow
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
        # activate for required roles the first message
        self.wftool.doActionFor(self.messages[0], 'activate')
        # viewlet contain one message
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0], )))
        logout()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0], )))

    def test_getAllMessages_date(self):
        viewlet = self._set_viewlet()
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types))
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

    def test_getAllMessages_tal_condition(self):
        viewlet = self._set_viewlet()
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types))
        message = self.messages[2]
        message.tal_condition = "python:False"
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        message.tal_condition = "python:context==portal"
        self.assertEqual(len(viewlet.getAllMessages()), 3)

    def test_getAllMessages_location(self):
        viewlet = self._set_viewlet()
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types))
        message = self.messages[2]
        message.location = "homepage"
        message.reindexObject()
        self.assertEqual(len(viewlet.getAllMessages()), 3)
        viewlet.context = self.message_config_folder
        self.assertEqual(len(viewlet.getAllMessages()), 2)

    def test_viewlet_rendering(self):
        """
        Test if viewlet rendering is ok (text and css class)
        """
        viewlet = MessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        # activate one message.
        self.wftool.doActionFor(self.messages[0], 'activate')
        # viewlet.render()
        viewlet_rendering = viewlet.context()
        self.assertIn(self.messages[0].text.output, viewlet_rendering)
        self.assertIn('messagesviewlet-info', viewlet_rendering)
        self.assertNotIn(self.messages[1].text.output, viewlet_rendering)
        self.assertNotIn(self.messages[2].text.output, viewlet_rendering)

    def test_hidden_uid_when_workflow_changes(self):
        # saves the hidden uid before it changes because of the workflow
        # modifications
        hidden_uid = self.messages[0].hidden_uid
        self.wftool.doActionFor(self.messages[0], 'activate')
        self.wftool.doActionFor(self.messages[0], 'deactivate')
        # checks if the hidden uid has whell changed.
        self.assertNotEqual(hidden_uid, self.messages[0])

    def test_required_roles_permissions(self):
        viewlet = self._set_viewlet()
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types))
        # Sets the required role to 'Authenticated' to message 1
        self.messages[0].required_roles = set(['Authenticated'])
        # Checks that we still see all messages as we are authenticated
        self.assertEqual(len(viewlet.getAllMessages()), 3)
        logout()
        # Checks that an anonymous user can't see anymore the restricted one.
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[1], self.messages[2])))

    def test_getAllMessages_local_roles(self):
        viewlet = self._set_viewlet()
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types))
        self.messages[0].use_local_roles = True
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        self.messages[0].manage_setLocalRoles(TEST_USER_ID, ['Reader'])
        self.assertEqual(len(viewlet.getAllMessages()), 3)

    def test_examples_profile(self):
        self.portal.portal_setup.runImportStepFromProfile('profile-collective.messagesviewlet:messages',
                                                          'collective-messagesviewlet-messages')
        self.assertEqual(len(self.portal.portal_catalog(portal_type='Message')), 6)
