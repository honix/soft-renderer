"""Shaders: small separate programs, the way they work in game dev.

A shader has two stages, run by Renderer.draw_triangle:

  vertex(vertex, polygon)  runs once per triangle corner and returns a dict of
                           "varyings" (numbers or numpy vectors).
  fragment(varyings)       runs once per covered pixel with the varyings
                           interpolated across the triangle. It returns an RGB
                           color in 0..1, or None to discard the pixel.

Whatever is set on the shader instance (light, camera, colors...) plays the
role of uniforms. A class can list varying names in `flat` to skip the
interpolation and take the value of the triangle's first vertex instead.

Everything is in world space, the meshes have no model matrix yet.
"""
import numpy as np


def normalize(v):
    length = np.linalg.norm(v)
    return v / length if length > 0 else v


class Shader:
    flat = ()

    def vertex(self, vertex, polygon):
        raise NotImplementedError

    def fragment(self, varyings):
        raise NotImplementedError


class NormalShader(Shader):
    """Debug: normal as color, no lighting."""

    def __init__(self, *args, **kwargs):
        pass

    def vertex(self, vertex, polygon):
        return {'normal': vertex.normal}

    def fragment(self, v):
        return (normalize(v['normal']) + 1) / 2


class LitShader(Shader):
    """Blinn-Phong lighting model with one directional light.

    Flat, Gouraud and Phong shaders below all use the same model and only
    differ in *where* it is evaluated: per face, per vertex or per pixel.
    """

    def __init__(self,
                 camera_position,
                 light_direction=(0.6, 1.0, 0.8),  # points towards the light
                 light_color=(1, 1, 1),
                 ambient=(0.12, 0.12, 0.15),
                 albedo=(0.75, 0.25, 0.2),
                 specular=0.6,
                 shininess=48):
        self.camera_position = np.asarray(camera_position, dtype=float)
        self.light_direction = normalize(np.asarray(light_direction, dtype=float))
        self.light_color = np.asarray(light_color, dtype=float)
        self.ambient = np.asarray(ambient, dtype=float)
        self.albedo = np.asarray(albedo, dtype=float)
        self.specular = specular
        self.shininess = shininess

    def light(self, position, normal):
        n = normalize(normal)
        to_light = self.light_direction
        to_camera = normalize(self.camera_position - position)

        diffuse = max(np.dot(n, to_light), 0)
        # Blinn: half vector instead of Phong's reflected vector
        half = normalize(to_light + to_camera)
        specular = max(np.dot(n, half), 0) ** self.shininess if diffuse > 0 else 0

        color = self.albedo * (self.ambient + self.light_color * diffuse) \
            + self.light_color * self.specular * specular
        return np.clip(color, 0, 1)


class FlatShader(LitShader):
    """One color per face: light is computed with the face normal."""
    flat = ('color',)

    def vertex(self, vertex, polygon):
        return {'color': self.light(polygon.center, polygon.normal)}

    def fragment(self, v):
        return v['color']


class GouraudShader(LitShader):
    """Light per vertex, the resulting color is interpolated.

    Cheap and smooth, but a highlight smaller than a triangle is lost or
    smeared, and it can only show up on a vertex.
    """

    def vertex(self, vertex, polygon):
        return {'color': self.light(vertex.position, vertex.normal)}

    def fragment(self, v):
        return v['color']


class BlinnPhongShader(LitShader):
    """Normal is interpolated and light is computed per pixel."""

    def vertex(self, vertex, polygon):
        return {'position': vertex.position, 'normal': vertex.normal}

    def fragment(self, v):
        return self.light(v['position'], v['normal'])


SHADERS = {
    'normals': NormalShader,
    'flat': FlatShader,
    'gouraud': GouraudShader,
    'phong': BlinnPhongShader,
}
