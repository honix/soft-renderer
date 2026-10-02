# CLAUDE.md

Software renderer in Python. No GPU, no OpenGL; everything is rasterized in numpy/Pillow.

- Needs `numpy==1.23.5` (code uses `np.float` / `np.int`, removed in newer numpy).
- Run: `python main.py phong --out out.png` (see README for options).
- Test: `python -m tests.test_watertight` and `python -m tests.test_near_clip` (from the repo root) must print `ok` after any rasterizer change.

## Layout
- `main.py`: CLI and per-mesh draw loop (`render_mesh`). Bare `--mesh` names resolve in `assets/models/`.
- `softrender/`: the package.
  - `raster/renderer.py`: lines, triangle fill. `triangle_pixels()` decides coverage
    (top-left rule, no cracks or double draws); `draw_triangle()` clips at the near plane and runs a shader on top of it.
    `raster/buffer.py`: color/depth buffers.
  - `shaders.py`: `Shader` base (`vertex` / `fragment` stages, instance attributes act as
    uniforms). Flat, Gouraud, Blinn-Phong all share `LitShader.light()`.
  - `camera.py`: view/projection matrix and `project()`, which sets `vertex.clip`, `vertex.tposition` and `vertex.w`.
  - `geometry/`: `point`, `matrices`, `vertex`, `polygon`, `mesh`, `obj`. Normals are unit length,
    and vertices at the same position share a smooth normal.
- `assets/models/`: .obj meshes. `docs/images/`: README screenshots. `tests/`: run with `python -m tests.<name>`.

## Conventions
- Screen y points down; the camera looks down -z. Everything shading-related is in world space.
- Fragment colors are floats in 0..1; the renderer converts to 0..255.
- Perspective-correct interpolation needs `vertex.w`, set in `camera.project()`.
- Keep code plain and small, match the existing style.
