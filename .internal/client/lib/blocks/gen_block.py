from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionNode, CollisionBox
from panda3d.core import LVector3, Texture, DirectionalLight, AmbientLight, BitMask32, Vec3, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld
import json
import random
import socket
import time

class GenBlocks(ShowBase):
    def generateLineOfBlocks(self, direction, last=False):
        # Paramètres pour le bruit perlin
        scale = 4  # Échelle du bruit (ajustez selon vos besoins)
        octaves = 6  # Nombre d'octaves
        persistence = 0.5  # Persistance
        lacunarity = 2.0  # Lacunarity
        height_multiplier = 5 # Ajustez la hauteur souhaitée
        plusY = 5
        plusX = 5
        if direction == "x+":
            
            start_x = self.showbase.TerrainUserX + 11
            start_y = self.showbase.TerrainUserY
            plusY = 10
        elif direction == "x-":
            

            start_x = self.showbase.TerrainUserX - 1
            start_y = self.showbase.TerrainUserY
            plusY = 10
        elif direction == "y+":
            

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY + 11
            plusX = 10
        elif direction == "y-":
            

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY - 1
            plusX = 10
        else:
            return
        index = 0
        tableX = []
        tableY = []
        for y in range(start_y, start_y + plusY, 2):
            for x in range(start_x, start_x + plusX, 2):
                try:
                    tableX.append(x)
                    tableY.append(y)
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
                    index = 1
        if index == 1:
                if not last:
                        try:
                            random_port = random.randint(6000, 8000)
                            self.showbase.timeline_control("sggccet", "_P_"+str(random_port)+"_P_"+"_TX_"+json.dumps(list(set(tableX)))+"_TX_"+"_TY_"+json.dumps(list(set(tableY)))+"_TY_")
                            time.sleep(1)
                            # Code côté client pour se connecter au deuxième socket
                            GEN_second_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            GEN_second_client.connect(('127.0.0.1', random_port))  # Assurez-vous de mettre la bonne adresse du serveur
                            self.world_uptown = ""
                            received_data = b""
                            while True:
                                chunk = GEN_second_client.recv(1024)
                                if not chunk:
                                    break
                                if chunk == b'0x000011':
                                    break
                                received_data += chunk
                            self.world_uptown = received_data.decode("utf-8")
                            if self.world_uptown == "":
                                print("Cannot connect to server or data corrupt.")
                                return
                            self.showbase.JSON = json.loads(self.world_uptown)
                            self.showbase.JSON_World = self.showbase.JSON["lib"]
                            self.showbase.blocks_for_file_simplet = self.showbase.JSON_World["blocks"]

                            self.generateLineOfBlocks(direction,last=True)
                            return
                        except:
                            self.showbase.print("Error: ERROR_CLIENT_NOT_FATAL INFOS: [NOT_FATAL] [WHEN GENERATING SUPP TERRAIN] [CAUSE: 90% SERVER ERROR CONNEXION]")
        else:
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

        if int(self.showbase.enitiys.get("User")["pos"]["x"]) > -10 and int(self.showbase.enitiys.get("User")["pos"]["y"]) > -10 and int(self.showbase.enitiys.get("User")["pos"]["x"]) < 10 and int(self.showbase.enitiys.get("User")["pos"]["y"]) < 10:
            posY_1 = -5
            posY_2 = 5
            posX_1 = -5
            posX_2 = 5
        self.showbase.print("Spawn at : "+str(posX_1)+str(posX_2)+str(posY_1)+str(posX_2))
        for y in range(posY_1, posY_2, 1):
            for x in range(posX_1, posX_2, 1):
                try:
                    self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": -20}}"]
                    for z in range(-20, 40):
                        try:
                            self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": "+str(z)+"}}"]
                            self.createNewBlock(
                                x,
                                y,
                                z,
                                self.showbase.blocks_for_file_simplet["{\"pos\": {\"x\": "+str(x)+", \"y\": "+str(y)+", \"z\": "+str(z)+"}}"]["type"]
                            )

                            index += 1
                        except KeyError:
                            pass
                except KeyError:
                    pass
        for y in range(posY_1, posY_2, 1):
            for x in range(posX_1, posX_2, 1):
                self.createNewBlock(
                    x,
                    y,
                    -20,
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
        