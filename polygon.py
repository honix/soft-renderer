class Polygon:
    def __init__(self, indices, normal=None):
        # TODO: extend polygon indices max to >= 3
        assert len(indices) == 3

        self.indices = indices
        self.normal = normal