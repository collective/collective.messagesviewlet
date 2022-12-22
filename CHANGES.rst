Changelog
=========


1.0b1 (2022-12-22)
------------------

- Migrate to Plone 6.0.0: remove dexteritytextindexer, use new simplified
  resources registry, fix styles, fix icons, ...
  [boulch, laulaz]
- Add local messages feature. Local messages can be added in any folderish
  content types and you can choose if / on which levels they display.
  [boulch]
- Protect messages-config folder with one-state private workflow.
  [boulch]
- Add control panel (with messages-config folder link).
  [boulch]
- Use JS to show/hide messages when closed, to avoid caching problems (#12).
  [laulaz]
- Update / improve translations.
  [boulch, laulaz]


0.23 (2020-04-17)
-----------------
- Fix tests & travis build (#8).
  [laulaz]
- Prevent a bug when compare 2 dates with different timezone format.
  [boulch]


0.22 (2020-01-15)
-----------------

- Fix bug when message configuration don't permit to hide this message (close button stayed).
  [boulch]
- Adapted code for Plone5.2/Py3.
  [gbastien]

0.21 (2019-10-14)
-----------------

- Bypass allowed content types contraint when (post)install messagesConfig container
  [boulch]


0.20 (2019-08-23)
-----------------

- Added parameter `caching=True` to `utils.get_messages_to_show`, if `True`,
  the method result is cached in the request for given `context`.
  [gbastien]

0.19 (2019-07-15)
-----------------

- Added PseudoMessage class that be be used in viewlet template.
  [sgeulette]

0.18 (2019-05-27)
-----------------

- Define version to `2000` in `metadata.xml` of plone4 profile or upgrade step
  to 2000 is always displayed.
  [gbastien]

0.17 (2019-04-23)
-----------------

- Evaluate TAL condition using behavior `evaluate` method instead calling
  directly submethod `utils.evaluateExpressionFor` so behavior method
  `complete_extra_expr_ctx` is called.
  [gbastien]
- Call JS on portal_url so it can be cached by the browser.
  [gbastien]
- Tests on Plone5 and Plone4.
  [bsuttor]
- Manage profiles differently
  [sgeulette]
- Moved `MessagesViewlet.getAllMessages` code to `utils.get_messages_to_show`
  so it is easily callable from outside.
  [gbastien]
- Be defensive while managing TZ of message dates : do not set it if already
  set, it fails, moreover, indexing a metadata from a date attribute that had
  no TZ to one having TZ fails so undindex/reindex the entire message.
  [gbastien]

0.16 (2018-10-18)
-----------------

- Corrected import step dependencies to avoid unresolved warning. Save really changes !
  [sgeulette]

0.15 (2018-10-11)
-----------------

- Corrected import step dependencies to avoid unresolved warning.
  [sgeulette]

0.14 (2018-07-23)
-----------------

- Generate new uid when message is activated or re-activated.
  [sgeulette]

0.13 (2018-06-13)
-----------------

- Add <span> around cross <img> to ease override.
  [mgennart]

0.12 (2017-05-30)
-----------------

- Corrected image path.
  [sgeulette]
- Decrease space between messages
  [sgeulette]

0.11 (2017-03-16)
-----------------

- Added default message to warn that application only runs correctly on Firefox
  and Chrome, in addition to the already existing message that warned about the
  application only running correctly on Firefox.
  [gbastien]
- Use CheckBoxWidget for IMessage.required_roles` to ease selection when
  displaying several elements.
  [gbastien]
- Use RadioFieldWidget for Bool fields `IMessage.can_hide` and
  `IMessage.use_local_roles` so it is displayed correctly on the view,
  especially when it is False.
  [gbastien]


0.10 (2017-02-06)
-----------------

- Use INavigationRoot instead of IPloneSiteRoot to check if context is homepage.
  [bsuttor]


0.9 (2016-03-30)
----------------

- Increased coverage by using vocabulary methods instead of redefining it in tests.
  [gbastien]
- Added new example message: bad browser (not Firefox) warning
  [sgeulette]
- Use plone.formwidget.datetime to have hour at 0 by default.
  [sgeulette]
- CSS fix : display 'cursor: pointer;' when hovering the close button.
  [gbastien]
- Added 'MessagesConfig' to site_properties.types_not_searched.
  [gbastien]


0.8 (2016-01-18)
----------------

- Added parameter 'activate' to utils.add_message that makes it possible to create
  an 'activated' message directly.
  [gbastien]
- Adapted tests to use utils.add_message instead of duplicating this code.
  [gbastien]


0.7 (2015-11-17)
----------------

- Do not pass a default 'context' in utils._ to avoid strange ConnectionStateError.
  [gbastien]
- Give context to translate method.
  [sgeulette]
- Corrected and added icon type images.
  [sgeulette]


0.6 (2015-09-18)
----------------

- Simplify workflow. Only one activated state. Unrestricted search results before filtering.
  Added 'use local role' boolean attribute.
  [sgeulette]
- Updated default messages
  [sgeulette]
- Added local roles test
  [sgeulette]
- Renamed bad transition name
  [sgeulette]


0.5 (2015-09-14)
----------------

- Removed useless dependency on z3c.jbot.
  [gbastien]
- Corrected rst in readme.
  [sgeulette]


0.4 (2015-09-10)
----------------

- Use full url for readme images to display correctly on pypi.
  [sgeulette]


0.3 (2015-09-10)
----------------

- Translate title configuration folder.
  [sgeulette]


0.2 (2015-09-09)
----------------

- Added utils method to create message. Added example profile to add some messages.
  [sgeulette]


0.1 (2015-09-08)
----------------

- Initial release.
  [sgeulette, anuyens, DieKatze, boulch]
