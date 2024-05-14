SCC0250 - Computer Graphics (2024), Prof. Ricardo Marcondes Marcacini
# Necramtfi
## Introduction
- Necramtfi is a small Minecraft-like "game" written in OpenGL
- The development was split up into two incremental phases
    - 1. Pipeline, geometric transformations, MVP structure with cameras, objects and textures
    - 2. ...
### Phase 1
- TODO: add youtube link to video

# Dependencies (!) and Test Environment
- python (!) 3.11.7
    - numpy (!) 1.26.4
    - pillow (!) 10.2.0
    - pyopengl (!) 3.1.7
    - glfw (!) 2.7.0
- conda 24.3.0
- fedora 39

# Commands
- Mouse: Look around
- WASD: Walk
- Left Shift: Sprint
- Spacebar: Jump
- 1..6: Select hotbar object
- XYZ: Rotate selected object
- ,.: Scale selected object
- P: Toggle poligonal mode
- F: Toggle full screen
- Q: Close window

# Subsystems
## Lib
#### Graphics
- Abstracts the graphical library
#### IO
- Abstracts the window manager
- Supplies ways of dealing with user input
#### Game
- Provides boilerplate code for a 'game -> scenario -> objects and camera' hierarchy
#### Util
- Provides useful features and functions

## Template
- Uses lib to provide integration between the game, graphics and io libraries
- Lays out the programmable pipeline (vertex and fragment shaders) in a simple to use manner
- Gives a template for a program using mvp (model, view, projection)

## Scenarios
- Contains the scenarios, that is, behavior/code + objects and textures
#### World Map
- A simple minecraft map
##### Attributions
- Map
    - "Gravity Falls Adventure Map Chapters 1-8" (https://www.planetminecraft.com/project/gravity-falls-adventure-mode/) by \_\_\_\_Elsa\_\_\_\_
- Skybox (Modified)
    - "Skybox Minecraft daylight" (https://skfb.ly/oNSnn) by Tien Pham is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
- Book
    - "Book for minecraft" (https://skfb.ly/6ZPMu) by SebastianFEnriquez is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
- Cat
    - "Minecraft Cat" (https://skfb.ly/ow8Ms) by JanesBT is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
- Creeper
    - "Minecraft - Creeper" (https://skfb.ly/6QTSz) by Vincent Yanez is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
- Ender Dragon
    - "Minecraft - Ender Dragon" (https://skfb.ly/6Roty) by Vincent Yanez is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
- Castle
    - "Minecraft Castle" (https://skfb.ly/A6AL) by patrix is licensed under Creative Commons Attribution-ShareAlike (http://creativecommons.org/licenses/by-sa/4.0/).
- Pistol
    - "[Minecraft] Pistol" (https://skfb.ly/6UXyr) by sedona1029 is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
- TV (Modified)
    - "minecraft TV model" (https://skfb.ly/o6POQ) by DPancito is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
- Hotbar
    - Myself



# TO-DO
- Postar video
