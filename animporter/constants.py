import math



TPS = 20

# based on Mine-imator source code
def elastic(x):
	return - 2**(10 * (x - 1)) * math.sin((x - 1.075) * math.pi / 0.15)

# based on Mine-imator source code
def bounce(x):
	x = 1 - x
	if x < 1 / 2.75:
		return 1 - 7.5625 * x**2
	elif x < 2 / 2.75:
		return 1 - (7.5625 * (x - 1.5 / 2.75)**2 + 0.75)
	elif x < 2.5 / 2.75:
		return 1 - (7.5625 * (x - 2.25 / 2.75)**2 + 0.9375)
	else:
		return 1 - (7.5625 * (x - 2.625 / 2.75)**2 + 0.984375)

TRANSITIONS = {
	"linear": lambda x: x,
	"instant": lambda x: 0,
	"quad": lambda x: x**2,
	"cubic": lambda x: x**3,
	"quart": lambda x: x**4,
	"quint": lambda x: x**5,
	"sine": lambda x: 1 - math.cos(x * math.pi / 2),
	"expo": lambda x: 2**(10 * (x - 1)),
	"circ": lambda x: 1 - math.sqrt(1 - x**2),
	"elastic": elastic,
	"back": lambda x: x**2 * (2.70158 * x - 1.70158),
	"bounce": lambda x: bounce,
}
