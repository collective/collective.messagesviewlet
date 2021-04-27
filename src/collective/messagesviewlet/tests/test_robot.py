# -*- coding: utf-8 -*-
from plone import api
from collective.messagesviewlet import HAS_PLONE_5_AND_MORE
from collective.messagesviewlet.testing import COLLECTIVE_MESSAGESVIEWLET_ACCEPTANCE_TESTING  # noqa
from plone.app.testing import ROBOT_TEST_LEVEL
from plone.testing import layered

import os
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    if HAS_PLONE_5_AND_MORE:
        robot_tests = [
            os.path.join('robot', doc) for doc in os.listdir(robot_dir)
            if doc.endswith('.p5.robot') and doc.startswith('test_')
        ]
    else:
        robot_tests = [
            os.path.join('robot', doc) for doc in os.listdir(robot_dir)
            if doc.endswith('.p4.robot') and doc.startswith('test_')
        ]
    for robot_test in robot_tests:
        robottestsuite = robotsuite.RobotTestSuite(robot_test)
        robottestsuite.level = ROBOT_TEST_LEVEL
        suite.addTests([
            layered(
                robottestsuite,
                layer=COLLECTIVE_MESSAGESVIEWLET_ACCEPTANCE_TESTING,
            ),
        ])
    return suite
