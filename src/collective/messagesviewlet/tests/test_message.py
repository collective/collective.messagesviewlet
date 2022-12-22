# -*- coding: utf-8 -*-

from collective.messagesviewlet import HAS_PLONE_5_AND_MORE
from collective.messagesviewlet.browser.messagesviewlet import GlobalMessagesViewlet
from collective.messagesviewlet.message import add_timezone
from collective.messagesviewlet.message import IMessage
from collective.messagesviewlet.message import location
from collective.messagesviewlet.message import msg_types
from collective.messagesviewlet.testing import (
    COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING,
)  # noqa
from collective.messagesviewlet.utils import add_message
from dateutil.relativedelta import relativedelta
from datetime import datetime
# from DateTime import DateTime
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.annotation import IAnnotations
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager
from Products.Five.browser import BrowserView

import unittest

NUMBER_OF_PORTAL_TYPE_MESSAGE = 9


class MessageIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        self.member = api.user.get_current()
        self.request["AUTHENTICATED_USER"] = self.member

    def _clean_cache(self):
        # utils.get_messages_to_show is cached, remove infos in request annotation
        cache_keys = [
            k
            for k in IAnnotations(self.request)
            if k.startswith("messagesviewlet-utils-get_messages_to_show-")
        ]
        for cache_key in cache_keys:
            del IAnnotations(self.request)[cache_key]

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.isHidden = [True, True, False, False]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        tokens = [term.token for term in msg_types(self.portal)._terms]
        self.message_types = tokens + [tokens[0]]
        # The products build the "special" folder "messages-config" to store messages.
        self.message_config_folder = self.portal["messages-config"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.wftool = self.portal.portal_workflow
        self.messages = []
        # Create some messages
        for i, message_type in enumerate(self.message_types):
            title = "message%d" % (i + 1)
            text = (
                "<p>This is test message number %d...</p>"
                "<p>self-destruction programmed at the end of this test.</p>" % (i + 1)
            )
            if i < (len(self.message_types) - 1):
                message = add_message(
                    id=title,
                    title=title,
                    text=text,
                    start=add_timezone(datetime(2019, 10, 26, 12, 0)),
                    msg_type=self.message_types[i],
                    can_hide=self.isHidden[i],
                )
            else:
                self.another_folder = self._create_folder(self.portal, "myfolder")
                # Create some messages in others "local" folders.
                message = None
                try:
                    message = add_message(
                        id=title,
                        title=title,
                        text="This message isn't in default folder.It's in another folder!",
                        location="justhere",
                        # msg_type=self.message_types[i],
                        msg_type=self.message_types[0],
                        can_hide=self.isHidden[i],
                        container=self.another_folder,
                    )
                except:
                    assert message == None
                    lpf = api.portal.get_tool("portal_types")["Message"]
                    lpf.global_allow = True
                    message = add_message(
                        id=title,
                        title=title,
                        text="This message isn't in default folder.It's in another folder!",
                        location="justhere",
                        msg_type=self.message_types[i],
                        can_hide=self.isHidden[i],
                        container=self.another_folder,
                    )
            self.messages.append(message)

    def tearDown(self):
        self._changeUser("test")
        api.content.delete(obj=self.another_folder)
        messages = api.content.find(
            context=self.message_config_folder, portal_type="Message"
        )
        datas = [m.getObject() for m in messages]
        api.content.delete(objects=datas)

    def get_viewlet_manager(self, context, name):
        request = self.request
        view = BrowserView(context, request)
        manager = getMultiAdapter((context, request, view), IViewletManager, name)
        return manager

    def get_global_viewlet(self, context):
        return self.get_viewlet(context, "plone.portalheader")

    def get_local_viewlet(self, context):
        return self.get_viewlet(context, "plone.abovecontent")

    def get_viewlet(self, context, manager):
        self.activate_messages()
        manager = self.get_viewlet_manager(context, manager)
        manager.update()
        viewlet = [v for v in manager.viewlets if "message-viewlet" in v.__name__]
        assert len(viewlet) == 1  # nosec
        return viewlet[0]

    def activate_messages(self):
        for i, message_type in enumerate(self.message_types):
            api.content.transition(self.messages[i], "activate")

    def _create_folder(self, container, name):
        folder = api.content.create(
            container=container, type="Folder", id=name, title=name
        )
        return folder

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="Message")
        schema = fti.lookupSchema()
        self.assertEqual(IMessage, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="Message")
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="Message")
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IMessage.providedBy(obj))

    def test_adding(self):
        for i, message_type in enumerate(self.message_types):
            message = "message{}".format(i + 1)
            if i < (len(self.message_types) - 1):
                self.assertTrue(
                    IMessage.providedBy(self.message_config_folder[message])
                )
            else:
                self.assertTrue(IMessage.providedBy(self.portal["myfolder"][message]))

    def test_getAllMessages_wf(self):
        viewlet = GlobalMessagesViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        # no message in viewlet because all messages are in "inactive" state
        self.assertEqual(len(viewlet.getAllMessages()), 0)
        # activate for required roles the first message
        api.content.transition(self.messages[0], "activate")
        # viewlet contain one message
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0],)))
        logout()
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[0],)))

    def test_getAllGlobalMessages_date(self):
        viewlet = self.get_global_viewlet(self.portal)
        # len -1 because we've got 1 local message.
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types) - 1)
        # set message as message 0 and change date to ignore it.
        message = self.messages[0]
        message.start = datetime.now() + relativedelta(days=+1)
        # reindex object for catalog...
        message.reindexObject()
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        # test if printed messages are 1 and 2 without message 0
        self.assertSetEqual(
            set(viewlet.getAllMessages()), set((self.messages[1], self.messages[2]))
        )
        message = self.messages[1]
        message.end = datetime.now() + relativedelta(days=-2)
        # reindex object for catalog...
        message.reindexObject()
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        # test if printed message is 2 without messages 0 and 1
        self.assertSetEqual(set(viewlet.getAllMessages()), set((self.messages[2],)))

        # tests if message with date set to None is still available
        message = self.messages[2]
        message.start = message.end = None
        # reindex object for catalog...
        message.reindexObject()
        # tests that the message is still visible.
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)

    def test_getAllMessages_tal_condition(self):
        viewlet = self.get_global_viewlet(self.portal)
        # len -1 because we've got 1 local message.
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types) - 1)
        message = self.messages[2]
        message.tal_condition = "python:False"
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        message.tal_condition = "python:context==portal"
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 3)

    def test_getAllMessages_location(self):
        viewlet = self.get_global_viewlet(self.portal)
        # len -1 because we've got 1 local message.
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types) - 1)
        locations = [term.token for term in location(self.portal)._terms]
        self.assertTrue(
            set(locations).issubset(["fullsite", "homepage", "fromhere", "justhere"])
        )
        message = self.messages[2]
        message.location = "homepage"
        message.reindexObject()
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 3)
        viewlet.context = self.message_config_folder
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        alsoProvides(self.message_config_folder, INavigationRoot)
        viewlet.context = self.message_config_folder
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 3)

    def test_viewlet_rendering(self):
        """
        Test if viewlet rendering is ok (text and css class)
        """
        viewlet = self.get_global_viewlet(self.portal)
        self.assertIn(self.messages[0].text.output, viewlet.render())
        if not HAS_PLONE_5_AND_MORE:
            self.assertIn("messagesviewlet-info", viewlet.render())
        else:
            self.assertIn("portalMessage info", viewlet.render())
        self.assertIn(self.messages[2].text.output, viewlet.render())
        # self.wftool.doActionFor(self.messages[2], "deactivate")
        api.content.transition(self.messages[2], "deactivate")
        self._clean_cache()
        self.assertNotIn(self.messages[2].text.output, viewlet.render())

    def test_hidden_uid_when_workflow_changes(self):
        # saves the hidden uid before it changes because of the workflow
        # modifications
        hidden_uid = self.messages[0].hidden_uid
        api.content.transition(self.messages[0], "activate")
        api.content.transition(self.messages[0], "deactivate")
        # checks if the hidden uid has whell changed.
        self.assertNotEqual(hidden_uid, self.messages[0])

    def test_required_roles_permissions(self):
        viewlet = self.get_global_viewlet(self.portal)
        # len -1 because we've got 1 local message.
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types) - 1)
        # Sets the required role to 'Authenticated' to message 1
        self.messages[0].required_roles = set(["Authenticated"])
        # Checks that we still see all messages as we are authenticated
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 3)
        logout()
        # Checks that an anonymous user can't see anymore the restricted one.
        self._clean_cache()
        self.assertSetEqual(
            set(viewlet.getAllMessages()), set((self.messages[1], self.messages[2]))
        )

    def test_getAllGlobalMessages_local_roles(self):
        viewlet = self.get_global_viewlet(self.portal)
        # len -1 because we've got 1 local message.
        self.assertEqual(len(viewlet.getAllMessages()), len(self.message_types) - 1)
        self.messages[0].use_local_roles = True
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 2)
        self.messages[0].manage_setLocalRoles(TEST_USER_ID, ["Reader"])
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 3)

    def test_getAllGlobalMessages_navigation_root(self):
        alsoProvides(self.another_folder, INavigationRoot)
        message = add_message(
            id="navroot-message",
            title="navroot-message",
            text="This message is on a navigation root!",
            location="fullsite",
            msg_type=self.message_types[0],
            can_hide=self.isHidden[0],
            container=self.another_folder,
        )
        api.content.transition(message, "activate")

        other_messages_count = 3

        viewlet = self.get_global_viewlet(self.portal)
        self.assertEqual(len(viewlet.getAllMessages()), other_messages_count)

        viewlet = self.get_global_viewlet(self.another_folder)
        self.assertEqual(len(viewlet.getAllMessages()), other_messages_count + 1)

        sub_folder = self._create_folder(self.another_folder, "mysubfolder")
        alsoProvides(sub_folder, INavigationRoot)
        viewlet = self.get_global_viewlet(sub_folder)
        self.assertEqual(len(viewlet.getAllMessages()), other_messages_count + 1)

    def test_examples_profile(self):
        self.portal.portal_setup.runImportStepFromProfile(
            "profile-collective.messagesviewlet:messages",
            "collective-messagesviewlet-messages",
        )
        self.assertEqual(
            len(self.portal.portal_catalog(portal_type="Message")),
            NUMBER_OF_PORTAL_TYPE_MESSAGE,
        )

    def test_getAllMessages_with_justhere_local_message_in_folder(self):
        context = self.portal["myfolder"]
        viewlet = self.get_local_viewlet(context=context)
        self.assertEqual(len(viewlet.getAllMessages()), 1)

    def test_getAllMessages_and_play_with_local_messages(self):
        context = self.portal["myfolder"]
        container = self._create_folder(context, "mysubfolder")
        message = add_message(
            id="message5",
            title="message5",
            text="This message isn't in default folder.It's in another folder!",
            location="fromhere",
            msg_type=self.message_types[0],
            can_hide=self.isHidden[0],
            container=container,
        )
        api.content.transition(message, "activate")
        self.messages.append(message)
        # context = context
        viewlet = self.get_local_viewlet(context=context)
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        # context = container
        viewlet = self.get_local_viewlet(context=container)
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        container2 = self._create_folder(container, "mysubfolder2")
        # context = container2 (and message in container contains a "fromhere" message)
        viewlet = self.get_local_viewlet(context=container2)
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)
        message = self.messages[3]
        message.location = "fromhere"
        message.reindexObject()
        self._clean_cache()
        viewlet = self.get_local_viewlet(context=container2)
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 2)

    def test_local_messages_location(self):
        # To get this location message (justhere), we must be in a folder
        context = self.portal["myfolder"]
        locations = [term.token for term in location(context)._terms]
        self.assertEqual(locations, ["fromhere", "justhere"])

    def test_local_messages_viewlet_render(self):
        # Don't display any local messages
        api.portal.set_registry_record("messagesviewlet.show_local_message", False)
        api.portal.set_registry_record("messagesviewlet.authorize_local_message", True)
        context = self.portal["myfolder"]
        viewlet = self.get_local_viewlet(context=context)
        self.assertIn("", viewlet.render())

        # Don't display any local messages
        api.portal.set_registry_record("messagesviewlet.show_local_message", True)
        api.portal.set_registry_record("messagesviewlet.authorize_local_message", False)
        context = self.portal["myfolder"]
        viewlet = self.get_local_viewlet(context=context)
        self.assertIn("", viewlet.render())

        # Display local messages
        api.portal.set_registry_record("messagesviewlet.show_local_message", True)
        api.portal.set_registry_record("messagesviewlet.authorize_local_message", True)
        context = self.portal["myfolder"]
        viewlet = self.get_local_viewlet(context=context)
        self.assertIn("localmessagesviewlet", viewlet.render())
