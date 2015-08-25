# -*- coding: utf-8 -*-

from plone import api
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation

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
                                       title=FOLDER
                                       )
        excl = IExcludeFromNavigation(container)
        excl.exclude_from_nav = True
        types.getTypeInfo('MessagesConfig').global_allow = False
