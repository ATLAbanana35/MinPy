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

            
            hitNodePath.clearPythonTag('owner')
            index = self.showbase.blocks_for_file.index(hitObject.getPythonTag("data_content"))
            print(index)
            hitObject.removeNode()
            try:
                self.showbase.world.removeRigidBody(self.showbase.blocks[hitNodePath.getName()])
            except KeyError:
                print("ERROR_AT_LINE_30_'self.showbase.world.removeRigidBody(self.showbase.blocks[hitNodePath.getName()])'_CORRIGÉE")
            if self.showbase.blocks.get(hitNodePath.getName()) != None:
                del self.showbase.blocks[hitNodePath.getName()]
                del self.showbase.blocks_for_file[index]
class Action_Break_Blocks(ShowBase):

    def __init__(self, showbase):
        self.showbase = showbase
        # Créez une instance de BulletWorld
        raycaster = Raycaster(self.showbase.world, self.showbase.cameraNode, self.showbase)

        # Gestionnaire d'événements de souris
        self.accept("mouse1", raycaster.cast)
