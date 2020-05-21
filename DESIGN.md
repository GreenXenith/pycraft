# PyCraft Design

## Goals and Requirements
* ✓ Render cubes using PyGame surfaces and projection methods
* ✓ Map textures onto cubes
* ✓ Free-moving camera, controlled by mouse and WASD/Arrows
* ✓ Simple per-face lighting (This ended up being dynamic)
* ? Perform at an acceptable level (24FPS+)
* ✗ Block interaction (placement, removal)
* ✓ Face-culling system, likely using raycasting (Ended up using normals)
* ✗ Simple physics system
* ✓ Basic perlin-noise mapgen

`✓`: Goal complete  
`?`: Goal partially complete or undecided  
`✗`: Incomplete or rejected  

---

## Pseudocode and Structure
`camera.py`: Camera class (abstract)
* Contains position and pitch/yaw information
* Provides methods to set position/rotation

`vector.py`: Vec3 class
* Positional/rotational vectors
* All the math methods

`mesh.py`: Triangle, Mesh, and UV classes
* Triangle has 3 Vec3s, 3 UVs, normal, and color
* Mesh made up of n triangles
* Load from file (.obj)

`noise.py`: Perlin noise generator

`map.py`: Map and mapnode classes
* Map class stores mapnodes
* Coordinates are Y-up
* Uses noise for terrain generation

`renderer.py`: Rendering stage (class)
* Send mesh to renderer for drawing
* Rotate, position, and scale with matricies (world matrix)
* Change view with camera matrix (view matrix)
* Project to screenspace (projection matrix)

`main.py`: Main application
* Generate a map
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

---

`physics.py`(?): Physics handler (game object class)
* Acceleration, velocity, and position members
* `set_*` methods
* Physics properties (speed, gravity, etc)

`mapgen.py`(?): Map generator
* Uses Perlin noise
* Generates simple landscape
* Feed nodes to map
* Grass on top, layers of dirt underneath, followed by stone
