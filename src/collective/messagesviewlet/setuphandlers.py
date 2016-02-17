# -*- coding: utf-8 -*-

from plone import api
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from utils import _, add_message

FOLDER = "messages-config"


def post_install(context):
    """Post install script."""
    if context.readDataFile('collectivemessagesviewlet_default.txt') is None:
        return
    site = context.getSite()

    if not site.get(FOLDER):
        types = getToolByName(site, 'portal_types')
        types.getTypeInfo('MessagesConfig').global_allow = True
        container = api.content.create(site,
                                       "MessagesConfig",
                                       id=FOLDER,
                                       title=_('Messages viewlet settings', context=site)
                                       )
        excl = IExcludeFromNavigation(container)
        excl.exclude_from_nav = True
        types.getTypeInfo('MessagesConfig').global_allow = False


def add_default_messages(context):
    """ Add maintenance messages that can be activated when necessary """
    if context.readDataFile('collectivemessagesviewlet_messages.txt') is None:
        return
    site = context.getSite()
    add_message('maintenance-soon', _('maintenance_soon_tit', context=site), _('maintenance_soon_txt', context=site),
                msg_type='significant', can_hide=True, req_roles=['Authenticated'])
    add_message('maintenance-now', _('maintenance_now_tit', context=site), _('maintenance_now_txt', context=site),
                msg_type='warning', can_hide=False, req_roles=['Anonymous'])
    add_message('test-site', _('test_site_tit', context=site), _('test_site_txt', context=site),
                msg_type='warning', can_hide=False)
    add_message('browser-warning', _('bad_browser_tit', context=site), _('bad_browser_txt', context=site),
                msg_type='warning', can_hide=False,
                tal_condition="python:'Firefox' not in context.REQUEST.get('HTTP_USER_AGENT')")
