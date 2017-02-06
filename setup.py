# -*- coding: utf-8 -*-
"""Installer for the collective.messagesviewlet package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='collective.messagesviewlet',
    version='0.10',
    description="Add-on displaying manager defined messages in a viewlet",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='IMIO Team',
    author_email='support@imio.be',
    url='http://pypi.python.org/pypi/collective.messagesviewlet',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.behavior.talcondition',
        'plone.api',
        'plone.app.dexterity',
        'plone.app.lockingbehavior',
        'plone.formwidget.datetime >= 1.2',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
#            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'robotframework-selenium2screenshots',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
