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
            start_x = self.showbase.TerrainUserX + 11
            start_y = self.showbase.TerrainUserY
            plusY = 10
        elif direction == "x-":
            self.showbase.TerrainUserX = self.showbase.TerrainUserX-5

            start_x = self.showbase.TerrainUserX - 1
            start_y = self.showbase.TerrainUserY
            plusY = 10
        elif direction == "y+":
            self.showbase.TerrainUserY = self.showbase.TerrainUserY+5

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY + 11
            plusX = 10
        elif direction == "y-":
            self.showbase.TerrainUserY = self.showbase.TerrainUserY-5

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY - 1
            plusX = 10
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
                    for z in range(0, 30, 2):
                        # Calculez la hauteur en utilisant le bruit perlin
                        noise_value = noise.snoise3(x * scale, y * scale, z * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
                        # Normalisez la valeur entre -1 et 1 et multipliez-la par le coefficient d'élévation
                        normalized_height = (noise_value + 1) * height_multiplier
                        type = "nether-rack"
                        random_number = random.randint(0, 500)
                        if random_number == 1:
                            type = "obsidian"
                        random_number = random.randint(0, 20000)
                        if random_number == 1:
                            self.create_donjon(x,y)
                            print("DONJONS SPAWN!")
                        if z > 10:
                            self.createNewBlock(
                            x,
                            y,
                            z,  # Utilisez la hauteur calculée
                            type
                        )
                        else:
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
            start_x = self.showbase.TerrainUserX + 15
            start_y = self.showbase.TerrainUserY
            plusY = 10
        elif direction == "x+":
            start_x = self.showbase.TerrainUserX-4
            start_y = self.showbase.TerrainUserY
            plusY = 10
        elif direction == "y-":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY + 15
            plusX = 10
        elif direction == "y+":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY-4
            plusX = 10
        else:
            return
        for z in range(-20, 40):
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

        if int(self.showbase.enitiys.get("User")["pos"]["x"]) > -10 and int(self.showbase.enitiys.get("User")["pos"]["y"]) > -10 and int(self.showbase.enitiys.get("User")["pos"]["x"]) < 10 and int(self.showbase.enitiys.get("User")["pos"]["y"]) < 10:
            posY_1 = -10
            posY_2 = +10
            posX_1 = -10
            posX_2 = +10
        print("Spawn at : ", posX_1, posX_2, posY_1, posY_2)
        for y in range(posY_1, posY_2, 2):
            for x in range(posX_1, posX_2, 2):
                try:
                    self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": -20}}"]
                    for z in range(-20, 20, 2):
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
                    for z in range(0, 30):
                        # Calculez la hauteur en utilisant le bruit perlin
                        noise_value = noise.snoise3(x * scale, y * scale, z * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
                        # Normalisez la valeur entre -1 et 1 et multipliez-la par le coefficient d'élévation
                        normalized_height = (noise_value + 1) * height_multiplier
                        type = "nether-rack"
                        random_number = random.randint(0, 500)
                        if random_number == 1:
                            type = "obsidian"
                        random_number = random.randint(0, 20000)
                        if random_number == 1:
                            self.create_donjon(x,y)
                            print("donjon spawn!")
                        if z > 10:
                            self.createNewBlock(
                            x,
                            y,
                            z,  # Utilisez la hauteur calculée
                            type
                        )
                        else:
                            self.createNewBlock(
                            x,
                            y,
                            -int(normalized_height) * 2,  # Utilisez la hauteur calculée
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
        mainLight.setColor((1, 0, 0, 1))  # Couleur de la lumière
        mainLightNodePath = lightNode.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)  # Orientation de la lumière

        # Créez une lumière ambiante
        ambientLight = AmbientLight('ambient light')
        ambientLight.setColor((1, 0, 0, 1))  # Couleur de la lumière ambiante
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

    def create_donjon(self,x,y):
    # Création du so
        for Sx in range(-10, 10, 2):
            for Sy in range(-10, 10, 2):
                for Sz in range(0, 40, 2):
                    self.remove_block(Sx+x, Sy+y, Sz)
        def create_room(decal):
            size = 5
            if decal == 0:
                self.createNewBlock(x + 2, y+2, 1, "ender-portal")
                self.showbase.zombieGenerator.spawn(x + 2, y+2, 1)
                self.showbase.zombieGenerator.spawn(x + 2, y+2, 1)
                self.showbase.zombieGenerator.spawn(x + 2, y+2, 1)
            for Sx in range(0,size,2):
                for Sy in range(0,size,2):
                    self.createNewBlock(x + Sx + decal, y + Sy, 0, "stone")

            # Création des murs autour du sol
            for Sx in range(0,size,2):
                for Sz in range(0,10,2):
                    self.createNewBlock(x + Sx + decal, y - 1, 0+Sz, "stone")  # Mur inférieur
                    self.createNewBlock(x + Sx + decal, y + size, 0+Sz, "stone")  # Mur supérieur

            for Sy in range(0,size,2):
                for Sz in range(0,10,2):
                    self.createNewBlock(x - 1 + decal, y + Sy, 0+Sz, "stone")  # Mur gauche
                    self.createNewBlock(x + size + decal, y + Sy, 0+Sz, "stone")  # Mur droit
        create_room(0)
        create_room(5)
        create_room(-5)
    def __init__(self, showbase):
        self.showbase = showbase
        self.showbase.blocks = {}
        self.setupLights()
        self.generateTerrain()
        self.showbase.createNewBlock = self.createNewBlock
        