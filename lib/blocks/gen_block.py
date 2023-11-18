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
        # Paramètres pour le bruit perlin
        scale = 4  # Échelle du bruit (ajustez selon vos besoins)
        octaves = 6  # Nombre d'octaves
        persistence = 0.5  # Persistance
        lacunarity = 2.0  # Lacunarity
        height_multiplier = 5 # Ajustez la hauteur souhaitée
        plusY = 5
        plusX = 5
        if direction == "x+":
            self.showbase.TerrainUserX = self.showbase.TerrainUserX+5
            start_x = self.showbase.TerrainUserX + 21
            start_y = self.showbase.TerrainUserY
            plusY = 20
        elif direction == "x-":
            self.showbase.TerrainUserX = self.showbase.TerrainUserX-5

            start_x = self.showbase.TerrainUserX - 1
            start_y = self.showbase.TerrainUserY
            plusY = 20
        elif direction == "y+":
            self.showbase.TerrainUserY = self.showbase.TerrainUserY+5

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY + 21
            plusX = 20
        elif direction == "y-":
            self.showbase.TerrainUserY = self.showbase.TerrainUserY-5

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY - 1
            plusX = 20
        else:
            return
        for y in range(start_y, start_y + plusY, 2):
            for x in range(start_x, start_x + plusX, 2):
                try:
                    self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": -20}}"]
                    for z in range(-20, 40):
                        try: 
                            self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": "+str(z)+"}}"]
                            self.createNewBlock(
                                x,
                                y,
                                z,  # Utilisez la hauteur calculée
                                self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": "+str(z)+"}}"]["type"]
                            )
                        except KeyError:
                            owoiwedwiodwopdjodoqwqwqw2=False
                except KeyError:
                    randin = random.randint(1, 40)
                    if randin == 14:
                        self.createTree(x, y, 0)
                    for z in range(0, 10):
                        # Calculez la hauteur en utilisant le bruit perlin
                        noise_value = noise.snoise3(x * scale, y * scale, z * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
                        # Normalisez la valeur entre -1 et 1 et multipliez-la par le coefficient d'élévation
                        normalized_height = (noise_value + 1) * height_multiplier
                        type = 'grass' if z == 0 else 'dirt'
                        if -int(normalized_height) * 2 < -10:
                            type = "stone"
                        random_number = random.randint(0, 100)
                        if random_number == 1:
                            type = "iron-ore"
                        random_number = random.randint(0, 50)
                        if random_number == 1:
                            type = "coal-ore"
                        random_number = random.randint(0, 500)
                        if random_number == 1:
                            type = "diamond-ore"
                        self.createNewBlock(
                            x,
                            y,
                            -int(normalized_height) * 2,  # Utilisez la hauteur calculée
                            type
                        )
        for y in range(start_y, start_y + plusY, 2):
            for x in range(start_x, start_x + plusX, 2):
                self.createNewBlock(
                    x,
                    y,
                    -20,  # Utilisez la hauteur calculée
                    "bedrock"
                )

                    
    def removeLineOfBlocks(self, direction):
        # Paramètres pour le bruit perlin
        plusY = 10
        plusX = 10
        if direction == "x-":
            start_x = self.showbase.TerrainUserX + 20
            start_y = self.showbase.TerrainUserY
            plusY = 20
        elif direction == "x+":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY
            plusY = 20
        elif direction == "y-":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY + 20
            plusX = 20
        elif direction == "y+":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY
            plusX = 20
        else:
            return
        for z in range(-20, 20):
            for y in range(start_y, start_y + plusY, 2):
                for x in range(start_x, start_x + plusX, 2):
                    block_name = f'block-collision-node_{x}_{y}_{z}'
                    if block_name in self.showbase.blocks:
                        block_node = self.showbase.blocks[block_name]

                        # Supprimez le bloc de BulletWorld
                        # self.showbase.world.removeRigidBody(block_node)

                        # Retirez le bloc de la liste des blocs
                        del self.showbase.blocks[block_name]

                        # Supprimez le NodePath pour que le GeomNode ne soit plus rendu
                        for child in render.getChildren():
                            if child.getName() == block_name:
                                child.removeNode()
    def generateTerrain(self):
        def round_to_even(number):
            rounded_number = round(number)
            if rounded_number % 2 != 0:
                # Si le nombre arrondi est impair, ajoutez 1 pour le rendre pair
                rounded_number += 1
            return rounded_number

        # Paramètres pour le bruit perlin
        scale = 4  # Échelle du bruit (ajustez selon vos besoins)
        octaves = 6  # Nombre d'octaves
        persistence = 0.5  # Persistance
        lacunarity = 2.0  # Lacunarity
        height_multiplier = 5  # Ajustez la hauteur souhaitée
        index = 0
        posY_1 = round_to_even(self.showbase.enitiys.get("User")["pos"]["y"])-11
        posY_2 = round_to_even(self.showbase.enitiys.get("User")["pos"]["y"])+11
        posX_1 = round_to_even(self.showbase.enitiys.get("User")["pos"]["x"])-11
        posX_2 = round_to_even(self.showbase.enitiys.get("User")["pos"]["x"])+11

        if int(self.showbase.enitiys.get("User")["pos"]["x"]) > -20 and int(self.showbase.enitiys.get("User")["pos"]["y"]) > -20 and int(self.showbase.enitiys.get("User")["pos"]["x"]) < 20 and int(self.showbase.enitiys.get("User")["pos"]["y"]) < 20:
            posY_1 = -10
            posY_2 = +10
            posX_1 = -10
            posX_2 = +10

        for y in range(posY_1, posY_2, 2):
            for x in range(posX_1, posX_2, 2):
                try:
                    self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": -20}}"]
                    for z in range(-20, 40):
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
                    if random.randint(1, 40) == 14:
                        self.createTree(x, y, 0)
                    for z in range(0, 10):
                        # Calculez la hauteur en utilisant le bruit perlin
                        noise_value = noise.snoise3(x * scale, y * scale, z * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
                        # Normalisez la valeur entre -1 et 1 et multipliez-la par le coefficient d'élévation
                        normalized_height = (noise_value + 1) * height_multiplier
                        type = 'grass' if z == 0 else 'dirt'
                        if -int(normalized_height) * 2 < -10:
                            type = "stone"
                        random_number = random.randint(0, 100)
                        if random_number == 1:
                            type = "iron-ore"
                        random_number = random.randint(0, 50)
                        if random_number == 1:
                            type = "coal-ore"
                        random_number = random.randint(0, 500)
                        if random_number == 1:
                            type = "diamond-ore"
                        self.createNewBlock(
                            x,
                            y,
                            -int(normalized_height) * 2-2,  # Utilisez la hauteur calculée
                            type
                        )
        for y in range(int(self.showbase.enitiys.get("User")["pos"]["y"])-10, int(self.showbase.enitiys.get("User")["pos"]["y"])+10, 2):
            for x in range(int(self.showbase.enitiys.get("User")["pos"]["x"])-10, int(self.showbase.enitiys.get("User")["pos"]["x"])+10, 2):
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
        ambientLight.setColor((0.3, 0.3, 0.3, 1))  # Couleur de la lumière ambiante
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

        newBlockNode.setPythonTag('data_content', {"pos": {"x": x,"y": y,"z": z}, "type": type, "data": self.showbase.mods_blocks.get(type).get("data")}) 
        newBlockNode.setPythonTag('data', self.showbase.mods_blocks.get(type).get("data"))
        self.showbase.blocks_for_file_simplet[json.dumps({"pos": {"x": x,"y": y,"z": z}})] = {"pos": {"x": x,"y": y,"z": z}, "type": type, "data": {}}

    def createTree(self,x,y,z):
        self.createNewBlock(
                    x,
                    y,
                    z,  # Utilisez la hauteur calculée
                    "wood"
        )
        self.createNewBlock(
                    x,
                    y,
                    z+2,  # Utilisez la hauteur calculée
                    "wood"
        )
        self.createNewBlock(
                    x,
                    y,
                    z+4,  # Utilisez la hauteur calculée
                    "wood"
        )
        self.createNewBlock(
                    x,
                    y,
                    z+6,  # Utilisez la hauteur calculée
                    "wood"
        )
        self.createNewBlock(
                    x,
                    y,
                    z+8,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x+2,
                    y,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x-2,
                    y,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x,
                    y+2,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x,
                    y-2,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x-2,
                    y+2,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x+2,
                    y-2,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x+2,
                    y+2,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
        self.createNewBlock(
                    x-2,
                    y-2,
                    z+6,  # Utilisez la hauteur calculée
                    "oak"
        )
    def __init__(self, showbase):
        self.showbase = showbase
        self.showbase.blocks = {}
        self.setupLights()
        self.generateTerrain()
        self.showbase.createNewBlock = self.createNewBlock
        