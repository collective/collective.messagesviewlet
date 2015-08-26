.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.messagesviewlet
==============================================================================

Add-on displaying manager defined messages in a viewlet

Features
--------
![The three message types](docs/messageviewletinaction.png)

Messages are defined in control panel.

Multiple messages can be displayed together in the viewlet. 

A message contains the following attributes:

* text : displayed text
* message type : info, warning, important
* location : full site or homepage only
* start date : optional displaying start date
* end date : optional displaying end date

The collective.behavior.talcondition is enabled, providing 2 attributes. 
* tal condition : optional tal expression evaluated on viewlet context
* bypassing roles : optional roles bypassing the tal condition

![The management interface](docs/messageviewletinconfiguration.png)

A workflow is provided with the following states:

* inactive : not displayed
* activated for anonymous : displayed for anonymous users
* activated for members : displayed only for authenticated users
* activated for localroles : displayed only for authenticated users having local reader role


Translations
------------

This product has been translated into

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
