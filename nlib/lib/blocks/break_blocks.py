from direct.showbase.ShowBase import ShowBase
from threading import Timer
from panda3d.core import MouseButton
from panda3d.core import Point3

from direct.gui.DirectWaitBar import DirectWaitBar
import time
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t

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
        if self.showbase.rayQueue.getNumEntries() > 0 and self.showbase.isGUIopen == False:
            self.showbase.rayQueue.sortEntries()
            rayHit = self.showbase.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            # distanceFromPlayer = hitObject.getDistance(self.showbase.cameraNode)
            if hitObject == None:
                return
            if hitObject.getPythonTag("block_type") != None:
                if self.showbase.is_breaking_block == False:
                    if hitObject.getPythonTag("data").get("strength") != None:
                        if self.showbase.break_progress != None:
                            self.showbase.break_progress.destroy()
                        divide = 1
                        if self.showbase.mods_items.get(self.showbase.selectedBlockType) != None:
                            if self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("tool_p") != None:
                                divide = self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("tool_p")
                        self.showbase.break_timer = time.time()+(hitObject.getPythonTag("data").get("strength")/divide)
                        self.showbase.is_breaking_block = True
                        self.showbase.witch_block = hitObject.getPythonTag("data_content")
                        self.showbase.block_to_break = hitObject
                        self.showbase.time_to_break = hitObject.getPythonTag("data").get("strength")/divide
                        self.showbase.break_progress = DirectWaitBar(text="", value=0, range=100, pos=(0, 0, -0.9), barColor=(0, 1, 0, 1), scale=0.2)
                        return
                    else:
                        if self.showbase.break_progress != None:
                            self.showbase.break_progress.destroy()
                        divide = 1
                        if self.showbase.mods_items.get(self.showbase.selectedBlockType) != None:
                    
                            if self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("tool_p") != None:
                                divide = self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("tool_p")
                        print(divide)
                        self.showbase.break_timer = time.time()+2/divide
                        self.showbase.is_breaking_block = True
                        self.showbase.witch_block = hitObject.getPythonTag("data_content")
                        self.showbase.block_to_break = hitObject
                        self.showbase.time_to_break = 2/divide
                        self.showbase.break_progress = DirectWaitBar(text="", value=0, range=100, pos=(0, 0, -0.9), barColor=(0, 1, 0, 1), scale=0.2)
                        return
                else:
                    if (hitObject.getPythonTag("data_content") != self.showbase.witch_block or time.time() < self.showbase.break_timer):
                        return
                    else:
                        if hitObject.getPythonTag("data").get("tool_w") != None and self.showbase.mods_items.get(self.showbase.selectedBlockType) != None:
                            if self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("tool_w") != None and self.showbase.mods_items.get(self.showbase.selectedBlockType) != None:
                                if not self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("tool_w") >= hitObject.getPythonTag("data").get("tool_w"):
                                    print("Ce block DOIT se casser avec un outil avec une puissance de plus de :", hitObject.getPythonTag("data").get("tool_w"))
                                    self.showbase.is_breaking_block = False
                                    return
                            else:
                                print("Ce block DOIT se casser avec un outil avec une puissance de plus de :", hitObject.getPythonTag("data").get("tool_w"))
                                self.showbase.is_breaking_block = False
                                return
                        self.showbase.is_breaking_block = False
                        if hitObject.getPythonTag("data").get("sound") != None:
                            self.showbase.sound.play(path=hitObject.getPythonTag("data").get("sound"), pos=Point3(int(hitNodePath.getName().split("block-collision-node_")[1].split("_")[0]), int(hitNodePath.getName().split("block-collision-node_")[1].split("_")[1]), int(hitNodePath.getName().split("block-collision-node_")[1].split("_")[2])))
                        else:
                            self.showbase.sound.play(path="default-break-block.mp3", pos=Point3(int(hitNodePath.getName().split("block-collision-node_")[1].split("_")[0]), int(hitNodePath.getName().split("block-collision-node_")[1].split("_")[1]), int(hitNodePath.getName().split("block-collision-node_")[1].split("_")[2])))
            if hitObject.getPythonTag("type") == "zombie":
                life = hitObject.getPythonTag("life")
                id = hitObject.getPythonTag("id")
                print("Il reste",life,"de vie à zombie")
                if life > 0:
                    puissance = 2
                    if self.showbase.mods_items.get(self.showbase.selectedBlockType) != None:
                        if self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("strength") != None:
                            puissance = self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("strength")
                    life -= puissance
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
                    puissance = 2
                    if self.showbase.mods_items.get(self.showbase.selectedBlockType) != None:
                        if self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("strength") != None:
                            puissance = self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("strength")
                    life -= puissance
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
                ObjectType = hitObject.getPythonTag("block_type")
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
                        if len(self.showbase.userInventory) == 0:
                            self.showbase.userInventory[len(self.showbase.userInventory)] = [self.showbase.mods_items[ObjectType], 1]
                        else:
                            for indexX in range(0, 9):
                                if not indexX in self.showbase.userInventory and not str(indexX) in self.showbase.userInventory:
                                    self.showbase.userInventory[indexX] = [self.showbase.mods_items[ObjectType], 1]
                                    break
                    del self.showbase.blocks[hitNodePath.getName()]
                    del self.showbase.blocks_for_file_simplet[index]
class Action_Break_Blocks(ShowBase):

    def __init__(self, showbase):
        self.showbase = showbase
        # Créez une instance de BulletWorld
        self.raycaster = Raycaster(self.showbase.world, self.showbase.cameraNode, self.showbase)

        # Gestionnaire d'événements de souris
    def is_clicking(self):
        if base.mouseWatcherNode.hasMouse():
            if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
                if self.showbase.is_breaking_block == True:
                    percent_make = ((self.showbase.time_to_break - (self.showbase.break_timer - time.time()))*100 / self.showbase.time_to_break)
                    self.showbase.break_progress["value"] = percent_make
                self.raycaster.cast()
            else:
                self.showbase.is_breaking_block = False