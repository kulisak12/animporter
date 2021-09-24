from animporter.create_animation import create_animation
from animporter.constants import *
import json
import numpy as np
import sys

def import_file(filename, out_dir):
	project = parse_json(filename)
	speedup = get_speedup(project["project"]["tempo"])
	objects = project["timelines"]
	# add_children_links(objects) # not necessary

	for char in filter_type("char", objects):
		# one animation
		anim_path = char["name"]
		timeline = collect_bodyparts(objects, char["parts"], speedup)
		timeline.pop("hat")
		char_timeline = get_keyframes_list(char["keyframes"], speedup)
		timeline["char"] = char_timeline
		create_animation(out_dir, anim_path, timeline)


def parse_json(filename):
	with open(filename) as f:
		return json.load(f)

# frametime conversion
def get_speedup(tempo):
	if tempo != TPS:
		print(f"warn: animation tempo is {tempo}, will be converted to {TPS}", file=sys.stderr)
	return TPS / tempo

# rebuild the keyframes object into a nicer list
def get_keyframes_list(keyframes, speedup):
	keyframes_list = []
	for frame_num, properties in keyframes.items():
		keyframe = {}
		# recalculate frametime based on speedup
		keyframe["time"] = int(frame_num) * speedup
		# pack rotation and position into vectors
		keyframe["rot"] = np.array([
			properties.get("ROT_X", 0),
			properties.get("ROT_Y", 0),
			properties.get("ROT_Z", 0)
		])
		keyframe["pos"] = np.array([
			properties.get("POS_X", 0),
			properties.get("POS_Y", 0),
			properties.get("POS_Z", 0)
		])
		# default transition type is linear
		keyframe["transition"] = properties.get("TRANSITION", "linear")
		keyframes_list.append(keyframe)

	return sorted(keyframes_list, key=lambda x: x["time"])

# collect timelines of bodyparts
def collect_bodyparts(objects, bodyparts_ids, speedup):
	bodyparts = {}
	for part_id in bodyparts_ids:
		part = get_object_by_id(objects, part_id)
		part_name = part["model_part_name"]
		bodyparts[part_name] = get_keyframes_list(part["keyframes"], speedup)
	return bodyparts

def add_children_links(objects):
	for obj in objects:
		parent_name = obj["parent"]
		if parent_name != "root":
			parent = get_object_by_id(objects, parent_name)
			parent.setdefault("children", []).append(obj["id"])

def get_object_by_id(objects, id):
	for obj in objects:
		if obj["id"] == id:
			return obj

def map_objects_to_ids(objects, ids):
	return [ get_object_by_id(objects, id) for id in ids ]

def filter_type(type, iterable):
	return filter(lambda x: x["type"] == type, iterable)
