# Animporter – Developer documentation

Animporter is a command-line tool to create NPC animations in Minecraft by imporing them from Mine-imator.

## Building

Animporter uses Python's setuptools for building. Make sure you have the package installed.
```
pip install setuptools
```

Building and installing is done with the following command (you may need root privileges):
```
python setup.py build && python setup.py install
```

For development and debugging purposes, it is better to run the program in its modular form:
```
python -m animporter.main
```

## Minecraft functions

Minecraft allows players to run _commands_ which modify the world. Commands have a form of custom instructions and are therefore quite limited.

Commands can be grouped into _functions_. Functions are text files located inside a _datapack_, a module which can be loaded into the game.

Commands in a function are executed exclusively sequentially, which means that no control flow is directly supported. It is, however, possible to call functions from within functions. This in combination with conditional commands makes loops and if-else statements possible.

A function is always called within a _context_. The function's context determines where in the world the commands in the function are executed, as well as what entity executes the commands.

Animporter makes heavy use of two commands: `/tp` to move around the armor stands which make up the NPC, and `/data` to change the rotation of individual body parts.

Apart from that, _scoreboard_ is used to track animation time.

### Animation structure

For every frame of the animation, the positions and rotations are stored inside one function called `f` followed by the frame number. This function must be called from the context of the armor stand.

The main part of the function structure is the `tick` function. This function works like a for loop. When the function is called, it increments a global variable in the scoreboard and uses this value to find the correct frame function. As mention before, it is also necessary to switch the context to that of the armor stands. Unless a terminating condition is met, the function is scheduled to run again in the next tick.

The functions `play` and `stop` take care of the start and end of the animation. Most importantly, they identify the armor stands with tags which make it possible to target them accurately with commands.

#### Alternatives

The approach described above uses a global counter to track animation time. Its advantage is low CPU impact, since the majority of commands only need to run once.

An alternative approach is to track time as the armor stand's scores. This means that every command is run in every armor stand's context, doubling the CPU impact. However, this approach would be more flexible, as it would allow multiple NPC's to run the same animation out-of-sync, for example.

## Program structure

The program uses a simple approach of splitting the code into separate functions with the intent to maximize code reusability and clarity.

### Arguments

First of all, the `main` function parses command line arguments and provides them to subsequent functions. This is handled by the `argparse` package, which ensures behavior standard to command-line programs and also provides automatic help and error messages.

The validity of provided filenames is not checked directly, errors are caught and handled instead.

### Input parsing

Mine-imator projects are stored in text form in the JSON format. The file is parsed by the `json` package, which allows dictionary-style access to the data.

Each object in the project is described separately. They reference each other with their IDs. The approach is therefore to find all characters and fetch the respective body parts.

Each object has a list of keyframes associated with it. This list is parsed and stored. If the tempo of the animation does not match 20, the keyframe times are shifted accordingly.

### Frame rendering

When Mine-imator renders the animation, it fills the space between keyframes. Animporter does the same and calculates the resulting frames by interpolating between keyframes.

Mine-imator offers multiple transitions. The transitions are encoded as functions with both input and output ranging from 0 to 1. Many transitions have three variants: ease in, ease out, or both. These variants can be constructed by playing the transition in reverse or connecting two transitions together.

Once the frames are rendered, they need to be further processed. If the body has some rotation, the upper armor stand should be moved slightly. This shift in position is calculated by replacing body with a vector and rotating it in space.

Because the animation should be playable from any starting position and rotation, the coordinates need to be transformed to _local coordinates_ which are relative to the entity's view angle.

### Function creation

At last, the calculated values are put into functions and the functions are linked together.

The character's name is used to derive the tag for the armor stands which is given to them for the duration of the animation and is used for targeting the armor stands in commmands.

Float values are rounded to 5 decimal places. This could lead to imperfections if the animations are very precise.

### Caveats

Mine-imator and Minecraft treat coordinates differently. The first consequence is that the Y-axis and Z-axis are swapped. This is merely a cosmetic difference and can be taken care of during input parsing.

The second consequence is that the Y-rotation and Z-rotation use opposite signs. This appears to be Minecraft's quirk. All calculations are therefore done in the standard coordinate system and the signs are swapped when the values are printed to functions.

## Links

- Animporter: https://github.com/kulisak12/animporter
- Minecraft functions: https://minecraft.fandom.com/wiki/Function_(Java_Edition)
