Changelog
=========


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
