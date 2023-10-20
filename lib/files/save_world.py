import json
from panda3d.core import LineSegs, NodePath
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import Geom, GeomTriangles, BitMask32, Vec3
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomNode, TransformState, WindowProperties

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, Vec3, CollisionTraverser, CollisionRay, CollisionNode, CollisionHandlerQueue, Point2

class World_Saving(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def save_to_file(self):
        f = open("world.json", "w")
        f.write(json.dumps(self.showbase.blocks_for_file))
        f.close()
        f = open("worldSimplet.json", "w")
        f.write(json.dumps(self.showbase.blocks_for_file_simplet))
        f.close()
        exit()