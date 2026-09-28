# CLAUDE.md

Software renderer in Python. No GPU, no OpenGL; everything is rasterized in numpy/Pillow.

- Needs `numpy==1.23.5` (code uses `np.float` / `np.int`, removed in newer numpy).
- Run: `python main.py phong --out out.png` (see README for options).
- Test: `python test_watertight.py` must print `ok` after any rasterizer change.

## Layout
- `renderer.py`: buffers, lines, triangle fill. `triangle_pixels()` decides coverage
  (top-left rule, no cracks or double draws); `draw_triangle()` runs a shader on top of it.
- `shaders.py`: `Shader` base (`vertex` / `fragment` stages, instance attributes act as
  uniforms). Flat, Gouraud, Blinn-Phong all share `LitShader.light()`.
- `mesh.py`, `obj.py`, `vertex.py`, `polygon.py`: geometry. Normals are unit length,
  and vertices at the same position share a smooth normal.
- `main.py`: camera, projection, per-mesh draw loop, CLI.

## Conventions
- Screen y points down; the camera looks down -z. Everything shading-related is in world space.
- Fragment colors are floats in 0..1; the renderer converts to 0..255.
- Perspective-correct interpolation needs `vertex.w`, set in `main.py` when projecting.
- Keep code plain and small, match the existing style.
