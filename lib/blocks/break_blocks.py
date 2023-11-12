from direct.showbase.ShowBase import ShowBase

from direct.showbase.ShowBase import ShowBase
class Raycaster:
    def __init__(self, world, camera, showbase):
        self.world = world
        self.showbase = showbase
        self.camera = camera

    def cast(self):
        self.cameraSwingActivated = True

        md = self.showbase.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        if self.showbase.rayQueue.getNumEntries() > 0:
            self.showbase.rayQueue.sortEntries()
            rayHit = self.showbase.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.showbase.cameraNode)
            ObjectType = hitObject.getPythonTag("block_type")
            if hitObject.getPythonTag("type") == "zombie":
                life = hitObject.getPythonTag("life")
                id = hitObject.getPythonTag("id")
                print("Il reste",life,"de vie à zombie")
                if life > 0:
                    life -= 2
                    hitObject.setPythonTag("life", life)
                else:
                    hitObject.removeNode()
                    self.showbase.world.removeRigidBody(hitNodePath.getPythonTag("rigidBody"))
                    self.showbase.zombies[str(id)+"_isAlive"] = False
                    del self.showbase.zombies[str(id)+"_Isjump"]
                    del self.showbase.zombies[str(id)+"_objectif"]
                    del self.showbase.zombies[str(id)+"_zombieShape"]
                    del self.showbase.zombies[str(id)+"_collider"]
                    del self.showbase.zombies[str(id)+"_zombie"]
                    del self.showbase.zombiesUUID[self.showbase.zombiesUUID.index(id)]
                    del self.showbase.enitiys[str(id)+"_zombie"]
            elif hitObject.getPythonTag("type") == "pig":
                life = hitObject.getPythonTag("life")
                id = hitObject.getPythonTag("id")
                print("Il reste",life,"de vie à pig")
                if life > 0:
                    life -= 2
                    hitObject.setPythonTag("life", life)
                else:
                    hitObject.removeNode()
                    self.showbase.world.removeRigidBody(hitNodePath.getPythonTag("rigidBody"))
                    self.showbase.pigs[str(id)+"_isAlive"] = False
                    del self.showbase.pigs[str(id)+"_Isjump"]
                    del self.showbase.pigs[str(id)+"_objectif"]
                    del self.showbase.pigs[str(id)+"_pigShape"]
                    del self.showbase.pigs[str(id)+"_collider"]
                    del self.showbase.pigs[str(id)+"_pig"]
                    del self.showbase.pigsUUID[self.showbase.pigsUUID.index(id)]
                    del self.showbase.enitiys[str(id)+"_pig"]
            else:
                if ObjectType != "bedrock":
                    Pos = hitNodePath.getName().split("block-collision-node_")[1].split("_")
                    index = "{\"pos\": {\"x\": "+Pos[0]+", \"y\": "+Pos[1]+", \"z\": "+Pos[2]+"}}"
                    hitNodePath.clearPythonTag('owner')
                    hitObject.removeNode()
                else:
                    print("Vous ne pouvez pas casser la bedrock!")
                try:
                    if ObjectType != "bedrock":
                        self.showbase.world.removeRigidBody(self.showbase.blocks[hitNodePath.getName()])
                except KeyError:
                    print("ERROR_AT_LINE_30_'self.showbase.world.removeRigidBody(self.showbase.blocks[hitNodePath.getName()])'_CORRIGÉE")
                if self.showbase.blocks.get(hitNodePath.getName()) != None and ObjectType != "bedrock":
                    trne = 0
                    for indexX in self.showbase.userInventory:
                        element = self.showbase.userInventory[indexX]
                        if element[0]["id"].replace("Item", "") == ObjectType:
                            self.showbase.userInventory[indexX][1] += 1
                            trne = 1
                    if trne == 0:
                        self.showbase.userInventory[len(self.showbase.userInventory)] = [self.showbase.mods_items[ObjectType], 1]
                    del self.showbase.blocks[hitNodePath.getName()]
                    del self.showbase.blocks_for_file_simplet[index]
class Action_Break_Blocks(ShowBase):

    def __init__(self, showbase):
        self.showbase = showbase
        # Créez une instance de BulletWorld
        raycaster = Raycaster(self.showbase.world, self.showbase.cameraNode, self.showbase)

        # Gestionnaire d'événements de souris
        self.accept("x", raycaster.cast)
