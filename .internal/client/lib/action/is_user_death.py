from direct.showbase.ShowBase import ShowBase
from panda3d.core import TransformState
class IsUserDead(ShowBase):
    def __init__(self, showbase):
        self.dead_fall = "Vous êtes mort de chute"
        self.dead_zombie = "Vous, tué(e) par zombie"
        self.showbase = showbase
    def update_dead(self):
        if self.showbase.character.getZ() < -100:
            print(self.dead_fall)
            self.showbase.userShape.setTransform(TransformState.makePos(Point3(1, 1, 5)))
            self.showbase.blocksgenerated.generateTerrain()
        if self.showbase.userLife < 0:
            print(self.dead_zombie)
            self.showbase.userShape.setTransform(TransformState.makePos(Point3(1, 1, 5)))
            self.showbase.blocksgenerated.generateTerrain()