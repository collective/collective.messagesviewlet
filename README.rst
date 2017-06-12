.. image:: https://travis-ci.org/collective/collective.messagesviewlet.svg?branch=master
    :target: https://travis-ci.org/collective/collective.messagesviewlet
.. image:: https://coveralls.io/repos/collective/collective.messagesviewlet/badge.svg?branch=master
  :target: https://coveralls.io/github/collective/collective.messagesviewlet?branch=master


.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.messagesviewlet
==============================================================================

Add-on displaying manager defined messages in a viewlet

.. image:: https://raw.githubusercontent.com/collective/collective.messagesviewlet/master/docs/messageviewletinaction.png 
    :alt: The three message types.
    :width: 1300
    :height: 495
    :align: center

Features
--------

Messages are defined in control panel.

Multiple messages can be displayed together in the viewlet. 

A message contains the following configuration attributes:

* text : displayed text in the viewlet
* message type : info, warning, important (different layout in the viewlet)
* can hide : if checked, the user can hide the message (mark as read)
* start date : displaying start date (optional)
* end date : displaying end date (optional)
* required roles : user must have one of the required roles (optional)
* use local roles : message displayed for users having Reader local role on message (optional)
* location : full site or homepage only

The collective.behavior.talcondition is enabled, providing 2 attributes. 

* tal condition : optional tal expression evaluated on viewlet context
* bypassing roles : optional roles bypassing the tal condition

.. image:: https://raw.githubusercontent.com/collective/collective.messagesviewlet/master/docs/messageviewletinconfiguration.png 
    :alt: The management interface.
    :width: 1252
    :height: 1362
    :align: center


A workflow is provided with the following states:

* inactive : not displayed
* activated : displayed

The hiding functionality uses a cookie. It is necessary to deactivate a message to "reset" the cookie.
When activating again, the message will be displayed again even for users that hide it. 

The optional 'messages' profile adds some usefull examples that can be activated when needed:

* message for scheduled maintenance (limited to Member)
* message for imminent or current maintenance : (given to anonymous)
* message for staging site

Improvements
------------

* Modify hidden_uid when some fields are changed: end when gone, can_hide (to unchecked), start when end is gone
* Message definition from file system
* Message definition from rss feed

Translations
------------

This product has been translated into

- English
- French


Installation
------------

Install collective.messagesviewlet by adding it to your buildout::

   [buildout]

    ...

    eggs =
        collective.messagesviewlet


and then running "bin/buildout"


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.messagesviewlet/issues
- Source Code: https://github.com/collective/collective.messagesviewlet


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
