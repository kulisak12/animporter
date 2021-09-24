class Frame:
	def __init__(self, pos, rot):
		self.pos = pos
		self.rot = rot

def create_animation(out_dir, npc_name, anim_name, timeline):
	interpolated = {}
	for part, keyframes in timeline.items():
		interpolated[part] = interpolate(keyframes)
	pass

def interpolate(keyframes):
	# shift times to start at 0
	for f in keyframes:
		f["time"] -= keyframes[0]["time"]

	# calculate frames between keyframes
	interpolated = []
	time = 0
	for i in range(len(keyframes) - 1):
		begin = keyframes[i]
		end = keyframes[i + 1]
		transition = get_transition(begin["transition"])
		while time < end["time"]:
			interpolated.append(create_frame(begin, end, time, transition))
			time += 1
	# add last frame
	last_keyframe = keyframes[len(keyframes) - 1]
	interpolated.append(Frame(last_keyframe["pos"], last_keyframe["rot"]))

	return interpolated
	

def create_frame(begin, end, time, transition):
	new_frame = Frame(None, None)
	percentage = (time - begin["time"]) / (end["time"] - begin["time"])
	new_frame.pos = mix(begin["pos"], end["pos"], percentage, transition)
	new_frame.rot = mix(begin["rot"], end["rot"], percentage, transition)
	return new_frame

def mix(begin, end, percentage, transition):
	return (1 - transition(percentage)) * begin + transition(percentage) * end

def get_transition(name):
	return linear

def linear(x):
	return x
