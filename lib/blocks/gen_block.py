from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionNode, CollisionBox
from panda3d.core import LVector3, Texture, DirectionalLight, AmbientLight, BitMask32, Vec3, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletWorld
import noise
import asyncio
from threading import Lock

class GenBlocks(ShowBase):
    def generateLineOfBlocks(self, direction):
        # Paramètres pour le bruit perlin
        scale = 4  # Échelle du bruit (ajustez selon vos besoins)
        octaves = 6  # Nombre d'octaves
        persistence = 0.5  # Persistance
        lacunarity = 2.0  # Lacunarity
        height_multiplier = 5 # Ajustez la hauteur souhaitée
        plusY = 12
        plusX = 12
        print(direction)
        if direction == "x+":
            self.showbase.TerrainUserX = self.showbase.TerrainUserX+10
            start_x = self.showbase.TerrainUserX + 41
            start_y = self.showbase.TerrainUserY
            plusY = 40
        elif direction == "x-":
            self.showbase.TerrainUserX = self.showbase.TerrainUserX-10

            start_x = self.showbase.TerrainUserX - 1
            start_y = self.showbase.TerrainUserY
            plusY = 40
        elif direction == "y+":
            self.showbase.TerrainUserY = self.showbase.TerrainUserY+10

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY + 41
            plusX = 40
        elif direction == "y-":
            self.showbase.TerrainUserY = self.showbase.TerrainUserY-10

            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY - 1
            plusX = 40
        else:
            return
        for z in range(0, 20):
            for y in range(start_y, start_y + plusY, 2):
                for x in range(start_x, start_x + plusX, 2):
                    # Calculez la hauteur en utilisant le bruit perlin
                    noise_value = noise.snoise3(x * scale, y * scale, z * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
                    # Normalisez la valeur entre -1 et 1 et multipliez-la par le coefficient d'élévation
                    normalized_height = (noise_value + 1) * height_multiplier
                    self.createNewBlock(
                        x,
                        y,
                        -int(normalized_height) * 2,  # Utilisez la hauteur calculée
                        'grass' if z == 0 else 'dirt'
                    )
    def removeLineOfBlocks(self, direction):
        # Paramètres pour le bruit perlin
        plusY = 10
        plusX = 10
        print(direction)
        if direction == "x-":
            start_x = self.showbase.TerrainUserX + 40
            start_y = self.showbase.TerrainUserY
            plusY = 40
        elif direction == "x+":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY
            plusY = 40
        elif direction == "y-":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY + 40
            plusX = 40
        elif direction == "y+":
            start_x = self.showbase.TerrainUserX
            start_y = self.showbase.TerrainUserY
            plusX = 40
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
        # Paramètres pour le bruit perlin
        scale = 4  # Échelle du bruit (ajustez selon vos besoins)
        octaves = 6  # Nombre d'octaves
        persistence = 0.5  # Persistance
        lacunarity = 2.0  # Lacunarity
        height_multiplier = 5  # Ajustez la hauteur souhaitée
        for z in range(0, 10):
            for y in range(0, 20):
                for x in range(0, 20):
                    # Calculez la hauteur en utilisant le bruit perlin
                    noise_value = noise.snoise3(x * scale, y * scale, z * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
                    # Normalisez la valeur entre -1 et 1 et multipliez-la par le coefficient d'élévation
                    normalized_height = (noise_value + 1) * height_multiplier
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -int(normalized_height) * 2,  # Utilisez la hauteur calculée
                        'grass' if z == 0 else 'dirt'
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
        if type == 'grass':
            newBlockNode.lookAt(Vec3(x, y+1, z))
            self.showbase.grassBlock.instanceTo(newBlockNode)
        elif type == 'dirt':
            self.showbase.dirtBlock.instanceTo(newBlockNode)
        elif type == 'sand':
            self.showbase.sandBlock.instanceTo(newBlockNode)
        elif type == 'stone':
            self.showbase.stoneBlock.instanceTo(newBlockNode)

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
    def loadModels(self):
        self.showbase.grassBlock = loader.loadModel('./ressources/3d/models/blocks/grass-block.glb')
        self.showbase.dirtBlock = loader.loadModel('./ressources/3d/models/blocks/dirt-block.glb')
        self.showbase.stoneBlock = loader.loadModel('./ressources/3d/models/blocks/stone-block.glb')
        self.showbase.sandBlock = loader.loadModel('./ressources/3d/models/blocks/sand-block.glb')

        # ...

    def __init__(self, showbase):
        self.showbase = showbase
        self.showbase.blocks = {}
        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.showbase.createNewBlock = self.createNewBlock