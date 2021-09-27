import os

def create_files(out_dir, anim_path, frames):
	# create directories
	os.chdir(out_dir)
	if not os.path.exists(anim_path):
		os.makedirs(anim_path)
	os.chdir(out_dir + "/" + anim_path)

	for i in range(len(frames)):
		create_frame_file(frames, i)
	create_tick_file(len(frames), anim_path)
	create_play_file(anim_path)
	create_stop_file(anim_path)


def create_frame_file(frames, n):
	frame = frames[n]
	with open(get_function_name(n, ext=True), "w") as f:
		f.write(execute_if_stand("upper") + tp_command(frame["upper"].pos, frame["upper"].rot))
		f.write(execute_if_stand("upper") + pose_command(frame["head"].rot, frame["left_arm"].rot, frame["right_arm"].rot))
		f.write(execute_if_stand("lower") + tp_command(frame["lower"].pos, frame["lower"].rot))
		f.write(execute_if_stand("lower") + pose_command(frame["body"].rot, frame["left_leg"].rot, frame["right_leg"].rot))

def create_tick_file(num_frames, anim_path):
	anim_id = get_anim_id(anim_path)
	with open("tick.mcfunction", "w") as f:
		f.write("# scheduled function\n\n")
		f.write(f"scoreboard players add ${anim_id} npc 1\n")
		for i in range(1, num_frames):
			f.write(condition_command(i, anim_path))
		f.write(f"execute if score ${anim_id} npc matches ..{num_frames - 2} run schedule function npc:{anim_path}/tick 1\n")
		f.write(f"execute unless score ${anim_id} npc matches ..{num_frames - 2} run function npc:{anim_path}/stop\n")

def create_play_file(anim_path):
	anim_id = get_anim_id(anim_path)
	with open("play.mcfunction", "w") as f:
		f.write("# executed at upper armor stand, as upper/lower\n\n")
		f.write(f"tag @s add npc_{anim_id}\n")
		f.write(f"scoreboard players set ${anim_id} npc 0\n")
		f.write(f"function npc:{anim_path}/{get_function_name(0)}\n")
		f.write(f"schedule function npc:{anim_path}/tick 1\n")

def create_stop_file(anim_path):
	anim_id = get_anim_id(anim_path)
	with open("stop.mcfunction", "w") as f:
		f.write(f"tag @e[type=armor_stand] remove npc_{anim_id}\n")
		f.write(f"schedule clear npc:{anim_path}/tick\n")

def get_anim_id(anim_path):
	# tags cannot contain slashes
	return anim_path.replace("/", "_")

def get_function_name(n, ext=False):
	function_name = "f{:03d}".format(n)
	if ext:
		function_name += ".mcfunction"
	return function_name

def execute_if_stand(stand):
	return f"execute if entity @s[tag=npc_{stand}] run "

def tp_command(pos, rot):
	return f"tp @s {local_coords(pos, rot)}\n"

def pose_command(head, left, right):
	return f"data merge entity @s {{Pose:{{Head:{float_list(head)},LeftArm:{float_list(left)},RightArm:{float_list(right)}}}}}\n"

def condition_command(n, anim_path):
	anim_id = get_anim_id(anim_path)
	return f"execute if score ${anim_id} npc matches {n} as @e[type=armor_stand,tag=npc_{anim_id}] at @s run function npc:{anim_path}/{get_function_name(n)}\n"

def float_list(vec):
	return f"[{vec[0]}f,{vec[1]}f,{vec[2]}f]"

def local_coords(pos, rot):
	return f"^{pos[0]} ^{pos[1]} ^{pos[2]} ~{rot[1]} ~"
