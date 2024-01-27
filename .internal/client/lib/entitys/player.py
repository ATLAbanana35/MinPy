from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Point3, Vec3, TransformState, BitMask32
from panda3d.core import CollisionNode, CollisionBox
from direct.showbase.ShowBase import ShowBase
import uuid
class playerGen(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def spawn(self, x, y, z, id=uuid.uuid4()):
        self.showbase.playersUUID.append(id)
        self.showbase.players[str(id)+"_isAlive"] = True
        self.showbase.players[str(id)+"_Isjump"] = False
        self.showbase.players[str(id)+"_objectif"] = 10
        # Charger le modèle de personnage
        self.showbase.players[str(id)+"_player"] = self.showbase.loader.loadModel("ressources/3d/models/player/steve.glb")
        self.showbase.players[str(id)+"_player"].reparentTo(self.showbase.render)
        self.showbase.players[str(id)+"_player"].setScale(0.1, 0.1, 0.1)
        self.showbase.players[str(id)+"_player"].setHpr(0, 45, 0)

        # Créer une forme de capsule pour le personnage
        capsule_shape = BulletBoxShape(Vec3(2, 2, 4))

        # Créer un nœud RigidBody pour le personnage
        player_node = BulletRigidBodyNode("player")
        player_node.addShape(capsule_shape)
        player_node.setMass(10.0)  # Masse du personnage
        self.showbase.players[str(id)+"_collider"] = self.showbase.players[str(id)+"_player"].attachNewNode(player_node)
        self.showbase.players[str(id)+"_collider"].setPythonTag('owner', player_node)
        self.showbase.players[str(id)+"_collider"].setCollideMask(BitMask32.allOn())  # Activer la collision avec tout
        self.showbase.players[str(id)+"_collider"].setPos(5, 5, 0)
        self.showbase.players[str(id)+"_collider"].reparentTo(self.showbase.lightNode)
        player_node.setLinearFactor((0, 0, 1))  # Désactive les mouvements verticaux
        player_node.setAngularFactor((0, 0, 0))  # Désactive la rotation
        player_np = self.showbase.render.attachNewNode(player_node)
        self.showbase.world.attachRigidBody(player_node)
        self.showbase.players[str(id)+"_playerShape"] = player_node
        self.showbase.players[str(id)+"_player"].setPythonTag("type", "player")
        self.showbase.players[str(id)+"_player"].setPythonTag("life", 18)
        self.showbase.players[str(id)+"_player"].setPythonTag("id", id)
        # Définir la position initiale du personnage
        player_np.setPos(Point3(x, y, z))
        self.showbase.players[str(id)+"_playerShape"].setTransform(TransformState.makePos(Point3(x, y, z)))
        # Variables de gravité
        playerSolid = CollisionBox((-2, -2, -2), (2, 2, 2))
        playerNode = CollisionNode('player_'+str(id))
        playerNode.addSolid(playerSolid)
        collider = self.showbase.players[str(id)+"_player"].attachNewNode(playerNode)
        collider.setPythonTag('owner', self.showbase.players[str(id)+"_player"])
        collider.setPythonTag('rigidBody', player_node)
        # Enfin, montrez le modèle de personnage
        def player_gravity(task):
            if self.showbase.players[str(id)+"_isAlive"] == False:
                return task.done
            playerX = self.showbase.players[str(id)+"_playerShape"].getTransform().getPos().getX()
            playerY = self.showbase.players[str(id)+"_playerShape"].getTransform().getPos().getY()
            playerZ = self.showbase.players[str(id)+"_playerShape"].getTransform().getPos().getZ()
            playerZ -= 0.1

            for blockIndex in self.showbase.blocks:
                block = self.showbase.blocks[blockIndex]
                if block.getTransform().getPos().getX()-1.4 < playerX and block.getTransform().getPos().getX()+1.4 > playerX:
                    if block.getTransform().getPos().getY()-1.4 < playerY and block.getTransform().getPos().getY()+1.4 > playerY:
                        if block.getTransform().getPos().getZ()-1 < playerZ and block.getTransform().getPos().getZ()+0.5 > playerZ:
                            playerZ += 0.5
            for blockIndex in self.showbase.blocks:
                block = self.showbase.blocks[blockIndex]
                if block.getTransform().getPos().getX()-1 < playerX and block.getTransform().getPos().getX()+2 > playerX:
                    if block.getTransform().getPos().getY()-1 < playerY and block.getTransform().getPos().getY()+2 > playerY:
                        if block.getTransform().getPos().getZ()-1 < playerZ and block.getTransform().getPos().getZ()+2 > playerZ:
                            playerZ +=0.1
            if self.showbase.players[str(id)+"_Isjump"] == True:
                if self.showbase.players[str(id)+"_objectif"] > playerZ:
                    playerZ += 0.4
                else:
                    self.showbase.players[str(id)+"_Isjump"] = False
                        # Récupérer la position du joueur
            playerX = self.showbase.userShape.getTransform().getPos().getX()
            playerY = self.showbase.userShape.getTransform().getPos().getY()

            # Calculer le déplacement du player$ vers le joueur en X et Y
            delta_X = playerX - playerX
            delta_Y = playerY - playerY

            # Calculer la nouvelle position du player en X et Y
            new_X = playerX + delta_X * 0.005  # Ajustez la vitesse de déplacement
            new_Y = playerY + delta_Y * 0.005
            self.showbase.players[str(id)+"_player"].lookAt(self.showbase.cameraNode)
            self.showbase.players[str(id)+"_player"].setP(90)
            self.showbase.players[str(id)+"_player"].setR(0)
            self.showbase.players[str(id)+"_player"].setH(self.showbase.players[str(id)+"_player"].getH()+180)
            return task.cont
        def update_player_to_shape(task):
            if self.showbase.players[str(id)+"_isAlive"] == False:
                return task.done
            # Récupérez la position du RigidBodyNode
            rigid_body_position = self.showbase.players[str(id)+"_playerShape"].getTransform().getPos()
            rigid_body_position_2 = Vec3(rigid_body_position.x, rigid_body_position.y, rigid_body_position.z+1)
            # Mettez à jour la position du modèle du personnage
            self.showbase.players[str(id)+"_player"].setPos(rigid_body_position_2)
            self.showbase.enitiys[str(id)+"_player"] = {"type": "player", "pos": {"x": rigid_body_position.x, "y": rigid_body_position.y, "z": rigid_body_position.z}, "data": {}}
            self.showbase.players[str(id)+"_collider"].setPos(rigid_body_position)
            return task.cont
        taskMgr.add(player_gravity, "update_gravity")
        taskMgr.add(update_player_to_shape, "update_gravity")