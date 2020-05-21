# PyCraft
_Minecraft written in PyGame. Because why not._

## Usage
`python3 main.py`

## Controls
| Key  | Action |
|------|--------|
|`WASD`|Movement|
|Mouse |Rotate camera|
|`ESC` |Free/grab cursor|

## Notes
* It's slow. Such is the way of loops in Python.
* On my machine runs at 8FPS with 4 blocks, and at 3FPS with 64 blocks.
* Drawing could be sped up using Numpy vectorization, but drawing textured triangles with that would be rather difficult to figure out.
* The closer you get to blocks, the slower it will be. You may need to hold down `ESC` longer to free the cursor.
