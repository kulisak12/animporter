from animporter.constants import *
import copy
import math
import numpy as np
from scipy.spatial.transform import Rotation as R


class State:
    def __init__(self, pos, rot):
        self.pos = copy.deepcopy(pos)
        self.rot = copy.deepcopy(rot)


def render_frames(timeline):
    # synchronize animation begin and end
    min_time = min([keyframes[0]["time"] for keyframes in timeline.values()])
    for keyframes in timeline.values():
        shift_time(keyframes, min_time)
    max_time = max([keyframes[len(keyframes) - 1]["time"]
                   for keyframes in timeline.values()])
    last_frame_time = int(math.ceil(max_time))

    interpolated = {}
    for part, keyframes in timeline.items():
        interpolated[part] = interpolate(keyframes, last_frame_time)
    del timeline

    # process individual frames
    frames = separate_frames(interpolated, last_frame_time + 1)
    del interpolated
    for frame in frames:
        init_armor_stands(frame)
        adjust_for_body_rot(frame)
    for i in range(len(frames) - 1, 0, -1):
        transform_to_local(frames[i - 1], frames[i])
    setup_first_frame(frames[0])

    return frames


def init_armor_stands(frame):
    frame["upper"] = copy.deepcopy(frame["char"])
    frame["lower"] = copy.deepcopy(frame["char"])
    frame["lower"].pos[1] -= STANDS_OFFSET
    del frame["char"]


def adjust_for_body_rot(frame):
    body_rot = frame["body"].rot
    # move upper armor stand to still be on top of body
    offset = rotate(np.array([0, STANDS_OFFSET, 0]), body_rot)
    frame["upper"].pos = frame["lower"].pos + \
        rotate(offset, frame["lower"].rot)
    # inherit rotation
    for part in frame["head"], frame["left_arm"], frame["right_arm"]:
        part.rot += body_rot


# replace absolute coordinates with ones relative to angle of view
def transform_to_local(previous_frame, frame):
    for part in "upper", "lower":
        # position
        move = frame[part].pos - previous_frame[part].pos
        # position will be changed before rotation
        angle = previous_frame[part].rot[1]
        frame[part].pos = to_local(move, angle)
        # rotation
        frame[part].rot -= previous_frame[part].rot


def setup_first_frame(frame):
    # upper is the main armor stand
    offset = frame["lower"].pos - frame["upper"].pos
    frame["lower"].pos = to_local(offset, frame["upper"].rot[1])
    frame["upper"].pos = np.array([0, 0, 0])

    frame["lower"].rot -= frame["upper"].rot
    frame["upper"].rot = np.array([0, 0, 0])


# rotate vector in 3D
def rotate(vec, rot):
    matrix = R.from_euler("xyz", rot, degrees=True)
    return matrix.apply(vec)


def to_local(vec, angle):
    forward_vec = rotate(np.array([0, 0, 1]), [0, angle, 0])
    side_vec = rotate(forward_vec, [0, 90, 0])
    return np.array([
        np.dot(vec, side_vec),
        vec[1],
        np.dot(vec, forward_vec)
    ])


# group states by frames
# object of lists -> list of objects
def separate_frames(state_lists, num_frames):
    frames = [{} for _ in range(num_frames)]
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
    last_states = [State(last_keyframe["pos"], last_keyframe["rot"])
                   for _ in range(last_frame_time - time + 1)]

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
        def transition(x): return \
            base_transition(2*x) / 2 if x < 0.5 else 1/2 + \
            invert(base_transition)(2*x - 1) / 2
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
        return str[len(prefix):], True
    return str, False
