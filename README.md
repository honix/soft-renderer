### Run
```
pip install numpy==1.23.5 pillow
```
### Shaders
```
python main.py [normals|flat|gouraud|phong] [--mesh teapot.obj] [--size 512] [--out image.png]
```
A shader is a class from `shaders.py` with a `vertex()` and a `fragment()` stage
(see the docstring there); `Renderer.draw_triangle(v1, v2, v3, shader, polygon)`
runs it. Write your own by subclassing `Shader`.
