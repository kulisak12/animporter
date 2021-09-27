import math
from animporter.constants import TRANSITIONS


class State:
	def __init__(self, pos, rot):
		self.pos = pos
		self.rot = rot

def create_animation(out_dir, anim_path, timeline):
	# synchronize animation begin and end
	min_time = min([ keyframes[0]["time"] for keyframes in timeline.values() ])
	for keyframes in timeline.values():
		shift_time(keyframes, min_time)
	max_time = min([ keyframes[len(keyframes) - 1]["time"] for keyframes in timeline.values() ])
	last_frame_time = int(math.ceil(max_time))

	interpolated = {}
	for part, keyframes in timeline.items():
		interpolated[part] = interpolate(keyframes, last_frame_time)

	frames = separate_frames(interpolated, last_frame_time + 1)


# group states by frames
# object of lists -> list of objects
def separate_frames(state_lists, num_frames):
	frames = [ {} for _ in range(num_frames) ]
	for part, states in state_lists.items():
		for i in range(num_frames):
			frames[i][part] = states[i]
	
	return frames

# shift times to start at 0
def shift_time(keyframes, shift):
	for f in keyframes:
		f["time"] -= shift


def interpolate(keyframes, last_frame_time):

	# calculate states between keyframes
	interpolated = []
	time = 0
	for i in range(len(keyframes) - 1):
		begin = keyframes[i]
		end = keyframes[i + 1]
		transition = get_transition(begin["transition"])
		while time < end["time"]:
			interpolated.append(create_state(begin, end, time, transition))
			time += 1
	# add last state
	last_keyframe = keyframes[len(keyframes) - 1]
	last_states = [ State(last_keyframe["pos"], last_keyframe["rot"]) for _ in range(last_frame_time - time + 1) ]
	
	return interpolated + last_states
	

def create_state(begin, end, time, transition):
	new_state = State(None, None)
	percentage = (time - begin["time"]) / (end["time"] - begin["time"])
	new_state.pos = mix(begin["pos"], end["pos"], percentage, transition)
	new_state.rot = mix(begin["rot"], end["rot"], percentage, transition)
	return new_state

def mix(begin, end, percentage, transition):
	return (1 - transition(percentage)) * begin + transition(percentage) * end

def get_transition(name):
	# transition modifiers
	name, _ = pop_prefix(name, "ease")
	name, ease_in = pop_prefix(name, "in")
	name, ease_out = pop_prefix(name, "out")

	# build function
	base_transition = TRANSITIONS[name]
	transition = None
	if ease_in and ease_out:
		transition = lambda x: \
			base_transition(2*x) / 2 if x < 0.5 else 1/2 + invert(base_transition)(2*x - 1) / 2
	elif ease_out:
		transition = invert(base_transition)
	else:
		transition = base_transition
	
	return transition

def invert(transition):
	return lambda x: 1 - transition(1 - x)
	
# if str starts with prefix, strip this prefix and return True
def pop_prefix(str, prefix):
	if str.startswith(prefix):
		return str[ len(prefix) : ], True
	return str, False
