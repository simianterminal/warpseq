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
			"The Basics": {
				"Home" : "index",
				"Installation": "installation",
				"FAQ": "faq",
				"Web UI": "ui",
				"Warp Club": "club",
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
		    "Expression Guide": {
			    "Intro to Expressions": "expr_intro",
				"Literal Notes" : "expr_literal",
				"Scale Notes And Chords" : "expr_scale_notes",
				"Rests & Ties" : "expr_rests_ties",
				"Mod Expressions": "expr_mod",
				"In Transforms": "expr_transforms",
				"More Randomness": "expr_random",
			    "Guide Tracks": "expr_track",
		     	"Variables": "expr_variables",
		    },
			"Developers": {
				"Python API": "api",
				"Contributing": "contributing",
			}
	},

	theme_options=dict(
		sidebar_background="#FF0000"
	)

)

site.build()
