# -*- coding: utf-8 -*-

from collective.messagesviewlet import HAS_PLONE_5_AND_MORE
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFPlone import interfaces as Plone
from Products.CMFPlone.utils import _createObjectByType
from collective.messagesviewlet.utils import _
from collective.messagesviewlet.utils import add_message
from zope.interface import implementer


FOLDER = 'messages-config'


def post_install(context):
    """Post install script."""
    if context.readDataFile('collectivemessagesviewlet_default.txt') is None:
        return
    site = api.portal.get()
    if not getattr(site, FOLDER, None):
        container = _createObjectByType(
            'MessagesConfig',
            container=site,
            id=FOLDER,
            title=_('Messages viewlet settings', context=site),
            description=_('This folder contains messages and should be kept private', context=site))
        excl = IExcludeFromNavigation(container)
        excl.exclude_from_nav = True


@implementer(Plone.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            u'collective.messagesviewlet:install-base',
        ]

    def getNonInstallableProducts(self):
        """Do not show on Plone's list of installable products."""
        return [
            'collective.messagesviewlet.upgrades',
        ]


def add_default_messages(context):
    """ Add maintenance messages that can be activated when necessary """
    if context.readDataFile('collectivemessagesviewlet_messages.txt') is None:
        return
    resource = 'resource'
    if HAS_PLONE_5_AND_MORE:
        resource = 'plone'
    site = api.portal.get()
    add_message('maintenance-soon', _('maintenance_soon_tit', context=site), _('maintenance_soon_txt', context=site),
                msg_type='significant', can_hide=True, req_roles=['Authenticated'])
    add_message('maintenance-now', _('maintenance_now_tit', context=site), _('maintenance_now_txt', context=site),
                msg_type='warning', can_hide=False, req_roles=['Anonymous'])
    add_message('test-site', _('test_site_tit', context=site), _('test_site_txt', context=site),
                msg_type='warning', can_hide=False)
    add_message('browser-warning', _('bad_browser_tit', context=site),
                _('bad_browser_txt ${resource}', mapping={'resource': resource}, context=site),
                msg_type='warning', can_hide=False,
                tal_condition="python:'Firefox' not in context.REQUEST.get('HTTP_USER_AGENT')")
    add_message('browser-warning-ff-chrome', _('bad_browser_ff_chrome_tit', context=site),
                _('bad_browser_ff_chrome_txt ${resource}', mapping={'resource': resource}, context=site),
                msg_type='warning', can_hide=False,
                tal_condition="python: 'Firefox' not in context.REQUEST.get('HTTP_USER_AGENT') and "
                "'Chrome' not in context.REQUEST.get('HTTP_USER_AGENT')")
