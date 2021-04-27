# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.messagesviewlet import HAS_PLONE_5_AND_MORE
from collective.messagesviewlet.testing import COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING  # noqa
from plone import api

if HAS_PLONE_5_AND_MORE:
    from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.messagesviewlet is properly installed."""

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if not HAS_PLONE_5_AND_MORE:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        else:
            self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.messagesviewlet is installed with portal_quickinstaller."""
        if not HAS_PLONE_5_AND_MORE:
            self.assertTrue(self.installer.isProductInstalled('collective.messagesviewlet'))
        else:
            self.assertTrue(self.installer.is_product_installed('collective.messagesviewlet'))

    def test_browserlayer(self):
        """Test that ICollectiveMessagesviewletLayer is registered."""
        from collective.messagesviewlet.interfaces import ICollectiveMessagesviewletLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveMessagesviewletLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if not HAS_PLONE_5_AND_MORE:
            self.installer = api.portal.get_tool('portal_quickinstaller')
            self.installer.uninstallProducts(['collective.messagesviewlet'])
        else:
            self.installer = get_installer(self.portal, self.layer["request"])
            self.installer.uninstall_product('collective.messagesviewlet')

    def test_product_uninstalled(self):
        """Test if collective.messagesviewlet is cleanly uninstalled."""
        if not HAS_PLONE_5_AND_MORE:
            self.assertFalse(self.installer.isProductInstalled('collective.messagesviewlet'))
        else:
            self.assertFalse(self.installer.is_product_installed('collective.messagesviewlet'))
