#!/usr/bin/env python3

from setuptools import setup

setup(
	name="animporter",
	version="1.0",
	description="Import NPCs from Mine-imator to Minecraft",
	author="David Klement",
	url="https://github.com/kulisak12/animporter",
	packages=[
		"animporter",
	],
	install_requires=[
	],
	include_package_data=True,
	license="MIT",
	classifiers=[
	  "Programming Language :: Python :: 3.8",
	],
	keywords=["minecraft", "npc", "animation"],
	entry_points={
		"console_scripts": [
			"animporter=animporter.main:main"
		],
	},
)

