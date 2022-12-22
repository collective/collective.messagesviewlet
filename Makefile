#!/usr/bin/make
#
# plone-path is added when "vhost_path: mount/site" is defined in puppet
plone=$(shell grep plone-path port.cfg|cut -c 14-)
hostname=$(shell hostname)
instance1_port=$(shell grep instance1-http port.cfg|cut -c 18-)
disable=1
copydata=1
instance=instance-debug
profile=collective.messagesviewlet:base

python=3.8
cfg=plone-5.2.x.cfg

all: run

.PHONY: setup
setup:
	virtualenv -p python$(python) .
	./bin/pip install --upgrade pip
	./bin/pip install -r requirements.txt

.PHONY: buildout
buildout:
	make setup
	bin/buildout -c $(cfg)

.PHONY: plone4
plone4:
	make cleanall
	make buildout python=2.7 cfg=plone-4.3.x.cfg

.PHONY: plone5.1
plone5.1:
	make cleanall
	make buildout python=2.7 cfg=plone-5.1.x.cfg

.PHONY: plone5.2
plone5.2:
	make cleanall
	make buildout python=3.8 cfg=plone-5.2.x.cfg

.PHONY: plone6.0
plone6.0:
	make cleanall
	make buildout python=3.8 cfg=plone-6.0.x.cfg

.PHONY: run
run:
	if ! test -f bin/instance1;then make buildout;fi
	bin/instance fg

.PHONY: cleanall
cleanall:
	rm -fr lib bin/buildout develop-eggs downloads eggs parts .installed.cfg
