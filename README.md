# Animporter

Animporter is a command-line tool to create NPC animations in Minecraft by imporing them from Mine-imator.

## Quick start

Create an animation in [Mine-imator](https://www.mineimator.com/). Create a project, import some characters and animate them. Give each character a unique name representing the animation. Save the project and find the project file, usually located in `C:/Users/user/Mine-imator/Projects/project-name/project-name.miproject`.

Download the source code, build and install (you may need root privileges):
```
python setup.py build && python setup.py install
```

Run the program, giving it the aforementioned project file as an argument. This will create a subdirectory in the current working directory for each character in your project. You may optionally specify an alternative output directory.
```
animporter project-name.miproject -o my-datapack/data/npc/functions
```

Animporter can also create a function which will spawn a template NPC. Again, the output directory can be customized.
```
animporter -t -o my-datapack/data/npc/functions
```

Open your world in Minecraft and spawn the NPC using this generated function.
```
/function npc:spawn
```

At this point, you should see 6 blocks of white wool. To make them look like an NPC, install and apply the [NPC resource pack](https://www.dropbox.com/s/uq3sardvfzwyz46/npc.zip?dl=1).

Add a scoreboard objective:
```
/scoreboard objectives add npc dummy
```

Stand withing 5 blocks of the NPC. Assuming the character was named `steve`, the animation can be played with the following command:
```
/execute as @e[type=armor_stand,distance=..5] at @e[type=armor_stand,tag=npc_upper,distance=..5] run function npc:steve/play
```

## Program arguments

Running `animporter -h` or `animporter --help` will print a basic usage guide. Extra details are provided here.

Multiple project files can be processed at once.
```
animported project1.miproject project2.miproject
```

The `-o` or `--output-dir` argument changes the directory in which subdirectories with functions are generated. If omitted, current working directory is used instead. This should be the `functions` directory inside your datapack under `npc` namespace.

If the `-t` or `--template` flag is present, a function called `spawn` will also be generated in the output directory. This function will spawn the armor stands that make up an NPC. You will need to change the content of the function to use the correct item (see section Resource pack below). It is also advised to add extra tags into `Tags` to better target the armor stands.

## Mine-imator

Mine-imator allows you to animate objects using keyframes. When the animation is rendered, the space between keyframes is smoothly filled. The smoothing-out algorithm can be modified by setting a _transition_ for the preceding keyframe.

The speed of playback is determined by _tempo_, a number of frames played every second. This value is customizable under the _Project_ tab. Since Minecraft's tickspeed is 20, the preferred tempo is also 20. Animporter is able to convert the tempo such that the playback speed is kept the same. The conversion is mostly seamless but can be noticed around keyframes.

There can be multiple animations in a single project file, simply add more characters into the same project. The name of the character will corespond to the subdirectory name when functions are generated. It is possible to nest subdirectories by including slashes in the name, such as `steve/jump`. This can be useful in case you want to add multiple animations for one NPC.

Since the NPC's are created with armor stands, it is impossible to support all Mine-imator's features. The following will have no effect in the final animation:
- bending arms and legs
- twisting the body
- changing the relative position of any body part
Body rotation is supported but may not look as good.

The repository contains the file `example.miproject` which you can import and modify.

## Resource pack

To create a custom NPC, first add its skin into `assets/minecraft/textures/skins`. In this folder you can also find skin templates for both the Alex model and the Steve model.

Next, create the models of the body parts. You can find the templates in `assets/minecraft/models/npc`. Choose either `steve` or `alex` (based on the skin used) and duplicate the folder, naming it after your NPC. For each of the files inside, change the referenced skin file.

Lastly, choose an item which will be used for the NPC model. Duplicate the template `assets/minecraft/models/item/white_wool.json` and rename it according to your chosen item. If you want to use the original unretextured item as well, you will need to update the item name in the file itself, too.

## Links

- Mine-imator: https://www.mineimator.com/
- NPC resource pack: https://www.dropbox.com/s/uq3sardvfzwyz46/npc.zip?dl=1
- Developer documentation: https://github.com/kulisak12/animporter/blob/master/devdoc.md

## License

&copy; 2021 David Klement, [MIT License](https://github.com/kulisak12/animporter/blob/master/LICENSE)
