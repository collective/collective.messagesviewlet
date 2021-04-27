# -*- coding: utf-8 -*-
from collective.messagesviewlet import HAS_PLONE_5_AND_MORE
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.messagesviewlet


class CollectiveMessagesviewletLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.messagesviewlet, name='testing.zcml')

    def setUpPloneSite(self, portal):
        if not HAS_PLONE_5_AND_MORE:
            installer = portal['portal_quickinstaller']
            installer.installProduct('collective.messagesviewlet')
        else:
            applyProfile(portal, 'collective.messagesviewlet:testing')
        api.user.create(email='test@imio.be', username='test')
        api.user.grant_roles(username='test', roles=['Site Administrator'])


COLLECTIVE_MESSAGESVIEWLET_FIXTURE = CollectiveMessagesviewletLayer()


COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MESSAGESVIEWLET_FIXTURE,),
    name='CollectiveMessagesviewletLayer:IntegrationTesting')

COLLECTIVE_MESSAGESVIEWLET_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MESSAGESVIEWLET_FIXTURE,),
    name='CollectiveMessagesviewletLayer:FunctionalTesting')

COLLECTIVE_MESSAGESVIEWLET_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_MESSAGESVIEWLET_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE),
    name='CollectiveMessagesviewletLayer:AcceptanceTesting')
