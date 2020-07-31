#!/usr/bin/python

import os

from rockchisel import Builder

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
			},
			"Setup And Usage": {
				"Installation": "installation",
				"Web UI": "ui",
				"Python API": "api",
				"FAQ" : "faq",
			},
			"Concepts" : {
				"Song" : "song",
				"Scale" : "scale",
				"Device" : "device",
				"Instrument" : "instrument",
				"Pattern" : "pattern",
				"Transform" : "transform",
				"Scene" : "scene",
				"Track" : "track",
				"Clip" : "clip"
			},
		    "Expression Language": {
			    "Intro to Expressions": "expr_intro",
				"Literal Notes" : "expr_literal",
				"Scale Notes And Chords" : "expr_scale_notes",
				"Rests & Ties" : "expr_rests_ties",
				"Mod Expressions": "expr_mod",
				"Transforms": "expr_transforms",
				"More Randomness": "expr_random",
			    "Guide Tracks": "expr_track",
		     	"Variables": "expr_variables",
		    },
			"Community": {
				"Warp Club": "club",
				"Contributing": "contributing",
			}
	},

	theme_options=dict(
		sidebar_background="#FF0000"
	)

)

site.build()
