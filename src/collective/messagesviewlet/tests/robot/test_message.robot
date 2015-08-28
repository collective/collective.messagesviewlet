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
# $ bin/robot src/plonetraining/testing/tests/robot/test_message.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: I can add a Message and hide/show it
  Given a logged-in site administrator
   I create a message 'My Message title' 'Wazaaaaaaaa' 'significant' 'fullsite'
   Then a message 'My Message title' has been created


*** Keywords *****************************************************************

I create a message '${title}' '${text}' '${msg_type}' '${location}'
  and an add message form
  When I type '${title}' into the title field
  and I type '${text}' into the richtext
  and I select '${msg_type}' into 'form-widgets-msg_type' selectbox
  and I select '${location}' into 'form-widgets-location' selectbox
  and I check 'form-widgets-can_hide-0'
  and I submit the form

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add message form
  Go To  ${PLONE_URL}/messages-config/++add++Message


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I type '${input}' into the richtext
  Select frame  id=form.widgets.text_ifr
  Input text  id=content  ${input}
  Unselect Frame

I select '${select}' into '${id}' selectbox
  Select from list by value  id=${id}  ${select}
  
I check '${id}'
  Select checkbox  id=${id}
  
I submit the form
  Click Button  Save


# --- THEN -------------------------------------------------------------------

a message '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

