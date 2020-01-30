Input RichText
  [Arguments]  ${input}
  Select frame  id=form.widgets.text_ifr
  Input text  id=content  ${input}
  Unselect Frame

# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.messagesviewlet -t test_message.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.messagesviewlet.testing.COLLECTIVE_MESSAGESVIEWLET_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/messagesviewlet/tests/robot/test_message.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  Selenium2Screenshots/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Selenium2Screenshots

Test Setup  Test Setup
Test Teardown  Close all browsers


*** Variables ****************************************************************

${xpath_day_list}  //div[contains(concat(' ',normalize-space(@class),' '),'picker__day')][contains(concat(' ',normalize-space(@class),' '),'picker__day--infocus')]



*** Test Cases ***************************************************************

Scenario: I can add a Message and hide/show it
  Given a logged-in site administrator
   I create a message 'My Message title' 'Wazaaaaaaaa' 'significant' 'fullsite'
   Then a message 'My Message title' has been created
    and I change the workflow to 'activate' for 'my-message-title'
   Then a viewlet with message 'Wazaaaaaaaa' is visible
    and I mark the message as read
   Then viewlet message with message 'Wazaaaaaaaa' is invisible
   Then reactivate message 'my-message-title'
    and a viewlet with message 'Wazaaaaaaaa' is visible


Scenario: Create docs with screenshots
  Given a logged-in site administrator
   an add message form
   Sleep  0.5
   Update element style  css=#content  border-color  black
   Update element style  css=#content  border-style  solid
   Update element style  css=#content  border-width  5px
   Update element style  css=#content  padding  10px
   Capture and crop page screenshot  docs/messageviewletinconfiguration.png  id=content
   Click button  id=form-buttons-cancel

   I create a message 'My Message title3' 'Hello, I\'m a warning message. I can contain stuff like "OMG, run for your life, everything gonna blow in a minute !!!".' 'warning' 'fullsite'
   and I change the workflow to 'activate' for 'my-message-title3'
   Then a viewlet with message 'Hello, I\'m a warning message.' is visible

   I create a message 'My Message title2' 'Hi there, I\'m a significant message. You can use me to inform people about things they must take into consideration. (e.g. "Don\'t forget the leaving pot of Cedric Friday at 3 PM. Free Belgian beers for E-V-E-R-Y-B-O-D-Y !!!").' 'significant' 'fullsite'
   and I change the workflow to 'activate' for 'my-message-title2'
   Then a viewlet with message 'I\'m a significant message.' is visible

   I create a message 'My Message title' 'I\'m an information message. I contain junks that nobody cares about. I\'m used to hold texts like "Don\'t forget to clock out" or "The toilets of the third floor are out of order".' 'info' 'fullsite'
   and I change the workflow to 'activate' for 'my-message-title'
   Then a viewlet with message 'I\'m an information message.' is visible

   Sleep  0.5
   Update element style  css=#visual-portal-wrapper  height  465px
   Update element style  css=#visual-portal-wrapper  overflow  visible
   Update element style  css=#visual-portal-wrapper  border-color  black
   Update element style  css=#visual-portal-wrapper  border-style  solid
   Update element style  css=#visual-portal-wrapper  border-width  5px
   Capture and crop page screenshot  docs/messageviewletinaction.png  id=visual-portal-wrapper


Scenario: Create message with end date precede start date. So Error.
  Given a logged-in site administrator
  I create a message 'My Message title' 'Wazaaaaaaaa' 'significant' 'fullsite' with end date precede start date
  Sleep  0.5
  Page should contain  The start date must precede the end date.


*** Keywords *****************************************************************

I create a message '${title}' '${text}' '${msg_type}' '${location}'
  and an add message form
  When I type '${title}' into the title field
   and I type '${text}' into the richtext
   and I select '${msg_type}' into 'form-widgets-msg_type' selectbox
   and I select '${location}' into 'form-widgets-location' selectbox
   and I check 'form.widgets.can_hide'
   and I submit the form

I create a message '${title}' '${text}' '${msg_type}' '${location}' with end date precede start date
  and an add message form
  When I type '${title}' into the title field
   and I type '${text}' into the richtext
   and I select '${msg_type}' into 'form-widgets-msg_type' selectbox
   and I select '${location}' into 'form-widgets-location' selectbox
   and I check 'form.widgets.can_hide'
   and I click calendar 'formfield-form-widgets-start' with input 'input.pattern-pickadate-date' and I select year 'div#formfield-form-widgets-start .picker__select--year' and month 'div#formfield-form-widgets-start .picker__select--month' and choice year '2021' and month '2' and day '12'
   and I click calendar 'formfield-form-widgets-end' with input 'input.pattern-pickadate-date' and I select year 'div#formfield-form-widgets-end .picker__select--year' and month '#formfield-form-widgets-end .picker__select--month' and choice year '2021' and month '1' and day '12'
   and I submit the form


# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  test

an add message form
  Go To  ${PLONE_URL}/messages-config/++add++Message


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I type '${input}' into the richtext
  Select Frame  css=.mce-edit-area iframe
  Input text  css=.mce-content-body  ${input}
  Unselect Frame

I select '${select}' into '${id}' selectbox
  Select from list by value  id=${id}  ${select}

I check '${name}'
  Select Radio Button  ${name}  true

I click calendar '${calendar_id}' with input '${input}' and I select year '${year_select}' and month '${month_select}' and choice year '${year}' and month '${month}' and day '${day}'
  Click Element  css=#${calendar_id} ${input}
  Select from list by value  css=${year_select}  ${year}
  Select from list by value  css=${month_select}  ${month}
  Click Element  xpath=//div[@id='${calendar_id}']//div[contains(@class, 'picker__day')]\[text()='${day}']
  Wait until page contains Element  css=#${calendar_id}
  Scroll Page To Location    0    800

I submit the form
  Click Button  Save


# --- THEN -------------------------------------------------------------------

a message '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I change the workflow to '${state}' for '${message_id}'
  ${UID} =  Path to uid  /${PLONE_SITE_ID}/messages-config/${message_id}
  Fire transition  ${UID}  ${state}

a viewlet with message '${msg}' is visible
  Go To  ${PLONE_URL}
  Wait until page contains  Site Map
  Page should contain  ${msg}

I mark the message as read
  Click Element  css=span.close-button

viewlet message with message '${msg}' is invisible
  Go To  ${PLONE_URL}
  Page should not contain  ${msg}

reactivate message '${message_id}'
  I change the workflow to 'deactivate' for '${message_id}'
  I change the workflow to 'activate' for '${message_id}'

Scroll Page To Location
  [Arguments]    ${x_location}    ${y_location}
  Execute JavaScript    window.scrollTo(${x_location},${y_location})


Test Setup
  Open test browser
  Set Window Size  1200  1200
