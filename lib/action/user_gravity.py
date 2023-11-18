from panda3d.core import TransformState, Vec3
from direct.showbase.ShowBase import ShowBase
from math import ceil, floor
from ..util.m_array import find_nearest
import time
class User_Gravity(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
        self.gravity = 0.1  # Valeur de gravité en m/s^2 (ajustez selon vos besoins)
        self.verticalSpeed = 0.0  # Vitesse verticale initiale
    def is_under_block(self):
        userX = self.showbase.userShape.getTransform().getPos().getX()
        userY = self.showbase.userShape.getTransform().getPos().getY()
        userZ = self.showbase.userShape.getTransform().getPos().getZ()
        userZ -= 0.1
        if (self.showbase.LastPosX-5 < userX and self.showbase.LastPosX+5 > userX) and (self.showbase.LastPosY-5 < userY and self.showbase.LastPosY+5 > userY):
                oOowoewi390tia34049=True
        else:
            userX = self.showbase.userShape.getTransform().getPos().getX()
            userY = self.showbase.userShape.getTransform().getPos().getY()

            deltaX = abs(userX - self.showbase.LastPosX)
            deltaY = abs(userY - self.showbase.LastPosY)
            if deltaX > deltaY:
                if userX > self.showbase.LastPosX:
                    self.showbase.blocksgenerated.generateLineOfBlocks("x+")
                    self.showbase.blocksgenerated.removeLineOfBlocks("x+")
                else:
                    self.showbase.blocksgenerated.generateLineOfBlocks("x-")
                    self.showbase.blocksgenerated.removeLineOfBlocks("x-")
                self.showbase.LastPosX = userX
                self.showbase.LastPosY = userY
            else:
                if userY > self.showbase.LastPosY:
                    self.showbase.blocksgenerated.generateLineOfBlocks("y+")
                    self.showbase.blocksgenerated.removeLineOfBlocks("y+")
                else:
                    self.showbase.blocksgenerated.generateLineOfBlocks("y-")
                    self.showbase.blocksgenerated.removeLineOfBlocks("y-")
                self.showbase.LastPosX = userX
                self.showbase.LastPosY = userY

        for blockIndex in self.showbase.blocks:
            block = self.showbase.blocks[blockIndex]
            if block.getTransform().getPos().getX()-1.4 < userX and block.getTransform().getPos().getX()+1.4 > userX:
                if block.getTransform().getPos().getY()-1.4 < userY and block.getTransform().getPos().getY()+1.4 > userY:
                    if block.getTransform().getPos().getZ()-1 < userZ and block.getTransform().getPos().getZ()+0.5 > userZ:
                        userZ += 0.5
        for blockIndex in self.showbase.blocks:
            block = self.showbase.blocks[blockIndex]
            if block.getTransform().getPos().getX()-1 < userX and block.getTransform().getPos().getX()+2 > userX:
                if block.getTransform().getPos().getY()-1 < userY and block.getTransform().getPos().getY()+2 > userY:
                    if block.getTransform().getPos().getZ()-1 < userZ and block.getTransform().getPos().getZ()+2 > userZ:
                        userZ +=0.1
        for zombieUUID in self.showbase.zombiesUUID:
            if self.showbase.zombies.get(str(zombieUUID)+"_zombie") != None:
                zombie = self.showbase.zombies[str(zombieUUID)+"_zombie"]
                zombieShape = self.showbase.zombies[str(zombieUUID)+"_zombieShape"]
                if zombie.getTransform().getPos().getX()-1 < userX and zombie.getTransform().getPos().getX()+2 > userX:
                    if zombie.getTransform().getPos().getY()-1 < userY and zombie.getTransform().getPos().getY()+2 > userY:
                        if zombie.getTransform().getPos().getZ()-1 < userZ and zombie.getTransform().getPos().getZ()+2 > userZ:
                            self.showbase.userLife -= 2
                            print("Il vous reste", self.showbase.userLife, "de vie")
                            zombieX = self.showbase.zombies[str(zombieUUID)+"_zombieShape"].getTransform().getPos().getX()
                            zombieY = self.showbase.zombies[str(zombieUUID)+"_zombieShape"].getTransform().getPos().getY()
                            zombieZ = self.showbase.zombies[str(zombieUUID)+"_zombieShape"].getTransform().getPos().getZ()
                            self.showbase.zombies[str(zombieUUID)+"_zombieShape"].setTransform(TransformState.makePos(Vec3(zombieX+4, zombieY, zombieZ)))
        if self.showbase.Isjump == True:
            if self.showbase.objectif > userZ:
                userZ += 0.4
            else:
                self.showbase.Isjump = False
        self.showbase.userShape.setTransform(TransformState.makePos(Vec3(userX, userY, userZ)))
    def update_user_to_shape(self):
        # Récupérez la position du RigidBodyNode
        rigid_body_position = self.showbase.userShape.getTransform().getPos()
        # Mettez à jour la position du modèle du personnage
        self.showbase.character.setPos(rigid_body_position)
        self.showbase.enitiys["User"]["pos"] = {"x": rigid_body_position.x, "y": rigid_body_position.y, "z": rigid_body_position.z}