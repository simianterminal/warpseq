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
			"About": {
				"Home" : "index",
				"Installation": "installation",
				"Concepts/Glossary": "concepts",
			},
			"Expressions" : {
				"Expressions: Intro": "expr_intro",
				"Randomness" : "expr_random",
				"Transforms" : "expr_arps",
				"Intra-Track" : "expr_track",
				"Variables" : "expr_variables",
			},
			"Community": {
				"Warp Club": "club",
				"Python API" : "api",
				"Contributing": "contributing",
			}
	},

	theme_options=dict(
		sidebar_background="#FF0000"
	)

)

site.build()
