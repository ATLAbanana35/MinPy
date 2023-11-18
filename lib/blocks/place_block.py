from panda3d.core import LineSegs, NodePath
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import Geom, GeomTriangles, BitMask32, Vec3
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomNode, TransformState, WindowProperties

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, Vec3, CollisionTraverser, CollisionRay, CollisionNode, CollisionHandlerQueue, Point2
from threading import Timer
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t
class Raycaster:
    def show_ray_direction(self, hit_pos, ray_direction):
        # Créez un objet LineSegs pour dessiner la ligne représentant la direction du rayon
        line = LineSegs()
        line.setColor(1, 0, 0, 1)  # Couleur de la ligne (rouge dans cet exemple)

        # Ajoutez un segment de ligne du point d'impact à la direction du rayon
        line.moveTo(hit_pos)
        line.drawTo(hit_pos + ray_direction * 10.0)  # Multipliez par une valeur pour définir la longueur de la ligne
        
        # Créez un nœud Panda3D pour la ligne
        ray_node = NodePath(line.create())
        ray_node.reparentTo(self.showbase.render)

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
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            hitBlockPos = hitObject.getPos()
            newBlockPos = hitBlockPos + normal * 2
            ObjectType = self.showbase.selectedBlockType
            trne = 0
            IN = 0
            if hitObject != None:
                if hitObject.getPythonTag('type') == "crafting-table":
                    self.showbase.gui_instance.open_craft_gui(self.showbase.mods_guis["Crafting-Table"])
                if hitObject.getPythonTag('type') == "furnace":
                    self.showbase.gui_instance.open_craft_gui(self.showbase.mods_guis["Furnace"])
            if self.showbase.mods_items.get(self.showbase.selectedBlockType)!= None:
                if self.showbase.mods_items[self.showbase.selectedBlockType]["data"].get("not_block") == True:
                    return

            for indexX in self.showbase.userInventory:
                element = self.showbase.userInventory[indexX]
                if element[0]["id"].replace("Item", "") == ObjectType:
                    self.showbase.userInventory[indexX][1] -= 1
                    trne = 1
                    if self.showbase.userInventory[indexX][1] < 0:
                        trne = 2
                        IN = indexX
            if trne == 2:
                del self.showbase.userInventory[IN]
                self.showbase.selectedBlockType = "nothing"
            if self.showbase.selectedBlockType != "nothing":
                self.showbase.createNewBlock(int(newBlockPos.x), int(newBlockPos.y), int(newBlockPos.z),
self.showbase.selectedBlockType)
                self.showbase.sound.play("default-place-block.mp3", Point3(newBlockPos.x, newBlockPos.y, newBlockPos.z))
            else:
                print("Break")

class Action_Place_Blocks(ShowBase):

    def __init__(self, showbase):
        self.showbase = showbase
        # Créez une instance de BulletWorld
        raycaster = Raycaster(self.showbase.world, self.showbase.camera, self.showbase)
        properties = WindowProperties()
        properties.setMouseMode(WindowProperties.M_relative)
        self.showbase.win.requestProperties(properties)
        self.showbase.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.showbase.camNode, Point2(0,0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.showbase.cameraNode.attachNewNode(rayNode)
        self.showbase.rayQueue = CollisionHandlerQueue()
        self.showbase.cTrav.addCollider(rayNodePath, self.showbase.rayQueue)

        # Gestionnaire d'événements de souris
        self.accept("mouse3", raycaster.cast)