from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionNode, CollisionBox
from panda3d.core import LVector3, Texture, DirectionalLight, AmbientLight, BitMask32, Vec3, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld
import noise
import asyncio
from threading import Lock
import json
import random

class GenBlocks(ShowBase):
    def generateLineOfBlocks(self, direction):
        print("Nothing")
                    
    def removeLineOfBlocks(self, direction):
        print("Nothing")
    def generateTerrain(self):
        index = 0
        posY_1 = -40
        posY_2 = +40
        posX_1 = -40
        posX_2 = +40
        print("Spawn at : ", posX_1, posX_2, posY_1, posY_2)
        for y in range(posY_1, posY_2, 2):
            for x in range(posX_1, posX_2, 2):
                try:
                    self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": -20}}"]
                    for z in range(0, 5, 2):
                        try:
                            self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": "+str(z)+"}}"]
                            self.createNewBlock(
                                x,
                                y,
                                z,  # Utilisez la hauteur calculée
                                self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": "+str(z)+"}}"]["type"]
                            )
                            index += 1
                        except KeyError:
                            owoiwedwiodwopdjodoqwqwqw2=False
                except KeyError:
                    for z in range(0, 5, 2):
                        # Calculez la hauteur en utilisant le bruit perlin
                        type = "end-stone"
                        self.createNewBlock(
                                x,
                                y,
                                z,  # Utilisez la hauteur calculée
                                type
                        )
        for y in range(int(self.showbase.enitiys.get("User")["pos"]["y"])-40, int(self.showbase.enitiys.get("User")["pos"]["y"])+40, 2):
            for x in range(int(self.showbase.enitiys.get("User")["pos"]["x"])-40, int(self.showbase.enitiys.get("User")["pos"]["x"])+40, 2):
                self.createNewBlock(
                    x,
                    y,
                    -20,  # Utilisez la hauteur calculée
                    "bedrock"
                )
    def setupLights(self):
        # Créez un nœud parent pour les objets que vous souhaitez éclairer
        lightNode = render.attachNewNode("lightNode")

        # Créez votre lumière directionnelle principale
        mainLight = DirectionalLight('main light')
        mainLight.setColor((1, 1, 1, 1))  # Couleur de la lumière
        mainLightNodePath = lightNode.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)  # Orientation de la lumière

        # Créez une lumière ambiante
        ambientLight = AmbientLight('ambient light')
        ambientLight.setColor((1, 1, 1, 1))  # Couleur de la lumière ambiante
        ambientLightNodePath = lightNode.attachNewNode(ambientLight)

        # Attachez tous les objets que vous souhaitez éclairer au nœud parent
        # Par exemple, si vous avez un modèle appelé monObjet, vous pouvez faire :
        # monObjet.reparentTo(lightNode)

        # Activez les lumières pour éclairer tous les objets sous le nœud parent
        render.setLight(mainLightNodePath)
        render.setLight(ambientLightNodePath)
        self.showbase.lightNode = lightNode


    def createNewBlock(self, x, y, z, type):
        newBlockNode = render.attachNewNode('block-collision-node_'+str(x)+"_"+str(y)+"_"+str(z))
        newBlockNode.setPos(x, y, z)
        self.showbase.mod_blocks_loaded[type + "Block"].instanceTo(newBlockNode)
        # Créez une forme de collision Bullet pour le bloc
        shape = BulletBoxShape(LVector3(2, 2, 2))  # Ajustez la taille selon vos besoins
        rigidBodyNode = BulletRigidBodyNode('block-collision-node_'+str(x)+"_"+str(y)+"_"+str(z))
        rigidBodyNode.addShape(shape)
        rigidBodyNode.setTransform(TransformState.makePos(Vec3(x,y,z)))
        # Créez un nœud Panda3D pour le bloc et associez-lui le corps rigide Bullet
        block_model = newBlockNode.attachNewNode(rigidBodyNode)
        block_model.setCollideMask(BitMask32.allOn())  # Activer la collision avec tout
        block_model.setPos(x, y, z)
        block_model.reparentTo(self.showbase.lightNode)
        # Ajoutez le bloc à BulletWorld
        self.showbase.world.attachRigidBody(rigidBodyNode)

        # Si vous avez besoin de personnaliser davantage les propriétés physiques du bloc,
        # vous pouvez le faire en accédant à rigidBodyNode (par exemple, rigidBodyNode.setMass(1.0)).
        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node_'+str(x)+"_"+str(y)+"_"+str(z))
        self.showbase.blocks['block-collision-node_'+str(x)+"_"+str(y)+"_"+str(z)] = rigidBodyNode
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)
        newBlockNode.setPythonTag('block_type', type)
        newBlockNode.setPythonTag('type', type)
        self.showbase._newBlock['block-collision-node_'+str(x)+"_"+str(y)+"_"+str(z)] = collider

        newBlockNode.setPythonTag('data_content', {"pos": {"x": x,"y": y,"z": z}, "type": type, "data": self.showbase.mods_blocks.get(type).get("data")}) 
        newBlockNode.setPythonTag('data', self.showbase.mods_blocks.get(type).get("data"))
        self.showbase.blocks_for_file_simplet[json.dumps({"pos": {"x": x,"y": y,"z": z}})] = {"pos": {"x": x,"y": y,"z": z}, "type": type, "data": {}}
    def remove_block(self, x,y,z):
                hitNodePath = self.showbase._newBlock.get('block-collision-node_'+str(x)+"_"+str(y)+"_"+str(z))
                if hitNodePath != None:
                    hitObject = hitNodePath.getPythonTag("owner")
                    Pos = hitNodePath.getName().split("block-collision-node_")[1].split("_")
                    index = "{\"pos\": {\"x\": "+Pos[0]+", \"y\": "+Pos[1]+", \"z\": "+Pos[2]+"}}"
                    hitNodePath.clearPythonTag('owner')
                    hitObject.removeNode()
                    try:
                        self.showbase.world.removeRigidBody(self.showbase.blocks[hitNodePath.getName()])
                    except KeyError:
                        print("ERROR_AT_LINE_30_'self.showbase.world.removeRigidBody(self.showbase.blocks[hitNodePath.getName()])'_CORRIGÉE")
                    del self.showbase.blocks[hitNodePath.getName()]
                    del self.showbase.blocks_for_file_simplet[index]
    def __init__(self, showbase):
        self.showbase = showbase
        self.showbase.blocks = {}
        self.setupLights()
        self.generateTerrain()
        self.showbase.createNewBlock = self.createNewBlock
        