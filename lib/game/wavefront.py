from pathlib import Path
from lib.graphics.bridge import coordinates_upload

import time
import math
import numpy as np

class wavefront():
    """Reads a .obj file.

    Instance attributes:
        filepath: str -- filepath used during reading
        physical_size: float -- biggest span on an axis
        diff_from_center: array[float] -- distance from center on each axis
    Instance methods:
        offload -- moves the local info to the correct buffers
    """

    def __init__(self, filepath):
        self.filepath = filepath

        self._clean()

        #Format: [min, max]
        self._physical_size_pc = [[0.0,0.0] for _ in range(3)]
        self.physical_size = 0.0

        self.diff_from_center = np.array((0.0,0.0,0.0))

        self.material_texture = dict()
        self._load()

        self.first = 0
        self.count = 0

        self.first_f = 0
        self.count_f = 0

        self.change_material = list()


    def _clean(self):
        self.vertices = []
        self.textures = []
        self.faces = []

    # Adapted from the class
    def _load(self):
        start_time = time.time()

        def v():
            self.vertices.append(values[1:4])
            vv = list(map(float,values[1:4]))
            for i in range(3):
                if vv[i] < self._physical_size_pc[i][0]:
                    self._physical_size_pc[i][0] = vv[i]
                elif vv[i] > self._physical_size_pc[i][1]:
                    self._physical_size_pc[i][1] = vv[i]

        def vt():
            self.textures.append(values[1:3])

        def usemtl():
            global material
            material = values[1]

        def f():
            global material
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            self.faces.append((face, face_texture, material))

        def vn():
            pass

        def mtllib():
            parent = str(Path(self.filepath).parent) + "/"
            filepath = parent + values[1]
            material = None
            for line in open(filepath, "r"):
                if line.startswith('#'): continue
                value = line.split()
                if not value: continue

                if value[0] == "newmtl":
                    material = value[1]

                if value[0] == "map_Kd":
                    self.material_texture[material] = parent + value[1]


        solution = {
            'v': v,

            'vt': vt,

            'vn': vn,

            'usemtl': usemtl,
            'usemat': usemtl,

            'f': f,

            'mtllib': mtllib,
        }

        for line in open(self.filepath, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] in solution:
                solution[values[0]]()

        print("load - %s seconds" % (time.time() - start_time))


    def offload(self, vcoordinates, fcoordinates):
        start_time = time.time()
        vertices_right_order = []
        textures_right_order = []

        material = None
        if len(self.faces) > 0:
            material = self.faces[0][2]
            self.change_material.append((len(vertices_right_order), material))
        for face in self.faces:
            if face[2] != material:
                material = face[2]
                if len(face[0]) > 0:
                    self.change_material.append((len(vertices_right_order), material))
            for vertex_id in face[0]:
                vertices_right_order.append(self.vertices[vertex_id-1])
            for texture_id in face[1]:
                textures_right_order.append(self.textures[texture_id-1])

        (self.first, self.count) = coordinates_upload(vcoordinates, vertices_right_order)
        (self.first_f, self.count_f) = coordinates_upload(fcoordinates, textures_right_order)

        self._calculate_physical_size()
        self._calculate_diff_from_center()

        self._clean()
        print("offload - %s seconds" % (time.time() - start_time))

    def _calculate_physical_size(self):
        max = 0.01 # minimum size to avoid possible zero divisions
        for i in range(len(self._physical_size_pc)):
            diff = math.fabs(self._physical_size_pc[i][0] - self._physical_size_pc[i][1])
            if diff > max:
                max = diff
        self.physical_size = max

    def _calculate_diff_from_center(self):
        for i in range(len(self._physical_size_pc)):
            diff = (self._physical_size_pc[i][0] + self._physical_size_pc[i][1])/2.0
            self.diff_from_center[i] = diff
