#!/usr/bin/python

from rockchisel import Builder
import os

path = os.path.dirname(os.path.realpath(__file__))

site = Builder(

    index = 'index',
	input_path  = path,
	output_path = os.path.join(path, "output"),
	theme = "rockchisel.themes.rockdoc",

	variables = dict(version = 0.1),
	page_title_template = "Warp MIDI Sequencer {{ version }}: {{ title }}",

	sections = {
			"User Guide": {
				"Home" : "index",
				"Installation": "installation",
				"Concepts": "concepts",
				"Expressions": "expressions",
			},
			"Community": {
				"License": "license",
				"Insiders": "insiders",
				"Contributing": "contributing",
			}
	}

)

site.build()
