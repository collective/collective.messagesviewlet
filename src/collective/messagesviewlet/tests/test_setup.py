# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.messagesviewlet.testing import COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.messagesviewlet is properly installed."""

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.messagesviewlet is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.messagesviewlet'))

    def test_browserlayer(self):
        """Test that ICollectiveMessagesviewletLayer is registered."""
        from collective.messagesviewlet.interfaces import ICollectiveMessagesviewletLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveMessagesviewletLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.messagesviewlet'])

    def test_product_uninstalled(self):
        """Test if collective.messagesviewlet is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('collective.messagesviewlet'))
