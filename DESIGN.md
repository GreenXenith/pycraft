# PyCraft Design

## Goals and Requirements
* Render cubes using PyGame surfaces and projection methods
* Map textures onto cubes
* Free-moving camera, controlled by mouse and WASD/Arrows
* Simple per-face lighting
* Perform at an acceptable level (24FPS+)
* Block interaction (placement, removal)
* Face-culling system, likely using raycasting
* Simple physics system
* (Maybe) Basic perlin-noise mapgen

## Pseudocode and Structure
`camera.py`: Camera class (abstract)
* Contains position and rotation information
* Provides methods to set position/rotation

`face.py`: Face class
* Provides position and rotation
* Provides image as face texture
* Loops through image and extract pixel colors
* Stores 16*16 pixels (list)
* Pixel colors tinted by a given color

`cube.py`: Cube class
* Provides position and rotation
* Provides image(s) as face texture(s)
* For all 6 sides, creates a face object and positions it relative to the cube position
* Provides different tint depending on side (for lighting)
* Face rotations are relative to cube position and place on cube

`node.py`: Node registry and class
* Provides function to register definitions
  * Name
  * Texture(s)
  * Solid
* Stores node definitions by name in global dictionary
* Generates id and stores in id<->nodename lists
* Function to get nodename from content id (and vice versa)

`map.py`: Map and mapnode classes
* Mapnode class stores node id, position, and rotation
* Map class stores mapnodes either arbitrarily or from a generator
* Coordinates are Y-up
* Map class provides methods to get and set mapnodes

`renderer.py`: Rendering stage (class)
* Provides render method given a face
* Loops through face pixels and projects into 3D space using projection matrix relative to camera

`main.py`: Main application
* Creates a map with nodes (or generates one)
* Initializes the camera (may inherit game object)
* Uses input to move camera (or set camera physics)
* Renderloop limited to 60FPS at most:
  * Loops through all mapnodes in map object and gets the definition
  * Creates a cube object using retrieved information
  * Loops through all faces and cull-checks
  * Renders face if needed

`input.py`: Input handler class
* `is_pressed` method
* Control mapping list
* `on_*` hooks?

`physics.py`: Physics handler (game object class)
* Acceleration, velocity, and position members
* `set_*` methods
* Physics properties (speed, gravity, etc)

`mapgen.py`: Map generator
* Uses Perlin noise
* Generates simple landscape
* Feed nodes to map
* Grass on top, layers of dirt underneath, followed by stone
