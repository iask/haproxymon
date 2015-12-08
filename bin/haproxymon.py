#!/usr/bin/env python
# -*- coding:utf-8 -*-
# vim: set noet sw=4 ts=4 sts=4 ff=unix fenc=utf8: 

import os
import sys
import toml
from optparse import OptionParser

if __name__ == "__main__":
	# load lib to sys.path
	sys.path.append( os.path.dirname(sys.path[0]) + '/lib')
	from HaproxyStats import HaproxyStats

	# parser cli args
	parser = OptionParser(version="%prog 1.0")
	parser.add_option("-f", "--file", dest="filename",  
                  help="read a configure file", metavar="FILE")  
	(options, args) = parser.parse_args()

	# parser configue file
	with open(options.filename) as conffile:
		SectionName = "haproxy"
		config = toml.loads(conffile.read())
		if SectionName not in config:
			sys.exit("section name do not existed: " + SectionName)

	# upload monitor data to falcon server
	hs = HaproxyStats(config[SectionName])
	hs.sendData()
