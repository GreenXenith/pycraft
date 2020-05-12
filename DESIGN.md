# PyCraft Design

## Goals and Requirements
* ✓ Render cubes using PyGame surfaces and projection methods
* ✗ Map textures onto cubes
* ? Free-moving camera, controlled by mouse and WASD/Arrows
* ✓ Simple per-face lighting (This ended up being dynamic)
* ? Perform at an acceptable level (24FPS+)
* ✗ Block interaction (placement, removal)
* ✓ Face-culling system, likely using raycasting (Ended up using normals)
* ? Simple physics system
* ? Basic perlin-noise mapgen

`?` means either partially complete or undecided.  

## Pseudocode and Structure
`camera.py`: Camera class (abstract)
* Contains position and rotation information
* Provides methods to set position/rotation

`vector.py`: Vec3 class
* Positional/rotational vectors
* All the math methods

`mesh.py`: Triangle and Mesh classes
* Triangle has 3 Vec3s, normal, and color
* Mesh made up of n triangles
* Load from file (.obj)

`cube.py`: Cube class
* Provides position and rotation
* Provides image(s) as face texture(s)
* Method to generate textured mesh

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
* Send mesh to renderer for drawing
* Rotate, position, and scale with matricies (world matrix)
* Change view with camera matrix (view matrix)
* Project to screenspace (projection matrix)

`main.py`: Main application
* Creates a map with nodes (or generates one)
* Initializes the camera
* Uses input to move camera (or set camera physics)
* Renderloop limited to 60FPS at most:
  * Loops through all mapnodes in map object and gets the definition
  * Creates a cube mesh using retrieved information
  * Renders faces depending on adjacent nodes

`input.py`: Input handler class
* `is_pressed` method
* Control mapping list
* `on_*` hooks?

`physics.py`(?): Physics handler (game object class)
* Acceleration, velocity, and position members
* `set_*` methods
* Physics properties (speed, gravity, etc)

`mapgen.py`(?): Map generator
* Uses Perlin noise
* Generates simple landscape
* Feed nodes to map
* Grass on top, layers of dirt underneath, followed by stone
