from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Point3, Vec3, TransformState, BitMask32
from panda3d.core import CollisionNode, CollisionBox
from direct.showbase.ShowBase import ShowBase
import uuid
class ZombieGen(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def spawn(self, x, y, z, id=uuid.uuid4()):
        self.showbase.zombiesUUID.append(id)
        self.showbase.zombies[str(id)+"_isAlive"] = True
        self.showbase.zombies[str(id)+"_Isjump"] = False
        self.showbase.zombies[str(id)+"_objectif"] = 10
        # Charger le modèle de personnage
        self.showbase.zombies[str(id)+"_zombie"] = self.showbase.loader.loadModel("../ressources/3d/models/zombie/zombie.glb")
        self.showbase.zombies[str(id)+"_zombie"].reparentTo(self.showbase.render)
        self.showbase.zombies[str(id)+"_zombie"].setScale(0.1, 0.1, 0.1)
        self.showbase.zombies[str(id)+"_zombie"].setHpr(0, 45, 0)

        # Créer une forme de capsule pour le personnage
        capsule_shape = BulletBoxShape(Vec3(2, 2, 4))

        # Créer un nœud RigidBody pour le personnage
        zombie_node = BulletRigidBodyNode("zombie")
        zombie_node.addShape(capsule_shape)
        zombie_node.setMass(10.0)  # Masse du personnage
        self.showbase.zombies[str(id)+"_collider"] = self.showbase.zombies[str(id)+"_zombie"].attachNewNode(zombie_node)
        self.showbase.zombies[str(id)+"_collider"].setPythonTag('owner', zombie_node)
        self.showbase.zombies[str(id)+"_collider"].setCollideMask(BitMask32.allOn())  # Activer la collision avec tout
        self.showbase.zombies[str(id)+"_collider"].setPos(5, 5, 0)
        self.showbase.zombies[str(id)+"_collider"].reparentTo(self.showbase.lightNode)
        zombie_node.setLinearFactor((0, 0, 1))  # Désactive les mouvements verticaux
        zombie_node.setAngularFactor((0, 0, 0))  # Désactive la rotation
        zombie_np = self.showbase.render.attachNewNode(zombie_node)
        self.showbase.world.attachRigidBody(zombie_node)
        self.showbase.zombies[str(id)+"_zombieShape"] = zombie_node
        self.showbase.zombies[str(id)+"_zombie"].setPythonTag("type", "zombie")
        self.showbase.zombies[str(id)+"_zombie"].setPythonTag("life", 18)
        self.showbase.zombies[str(id)+"_zombie"].setPythonTag("id", id)
        # Définir la position initiale du personnage
        zombie_np.setPos(Point3(x, y, z))
        self.showbase.zombies[str(id)+"_zombieShape"].setTransform(TransformState.makePos(Point3(x, y, z)))
        # Variables de gravité
        zombieSolid = CollisionBox((-2, -2, -2), (2, 2, 2))
        zombieNode = CollisionNode('Zombie_'+str(id))
        zombieNode.addSolid(zombieSolid)
        collider = self.showbase.zombies[str(id)+"_zombie"].attachNewNode(zombieNode)
        collider.setPythonTag('owner', self.showbase.zombies[str(id)+"_zombie"])
        collider.setPythonTag('rigidBody', zombie_node)
        # Enfin, montrez le modèle de personnage
        def zombie_gravity(task):
            if self.showbase.zombies[str(id)+"_isAlive"] == False:
                return task.done
            zombieX = self.showbase.zombies[str(id)+"_zombieShape"].getTransform().getPos().getX()
            zombieY = self.showbase.zombies[str(id)+"_zombieShape"].getTransform().getPos().getY()
            zombieZ = self.showbase.zombies[str(id)+"_zombieShape"].getTransform().getPos().getZ()
            zombieZ -= 0.1

            for blockIndex in self.showbase.blocks:
                block = self.showbase.blocks[blockIndex]
                if block.getTransform().getPos().getX()-1.4 < zombieX and block.getTransform().getPos().getX()+1.4 > zombieX:
                    if block.getTransform().getPos().getY()-1.4 < zombieY and block.getTransform().getPos().getY()+1.4 > zombieY:
                        if block.getTransform().getPos().getZ()-1 < zombieZ and block.getTransform().getPos().getZ()+0.5 > zombieZ:
                            zombieZ += 0.5
            for blockIndex in self.showbase.blocks:
                block = self.showbase.blocks[blockIndex]
                if block.getTransform().getPos().getX()-1 < zombieX and block.getTransform().getPos().getX()+2 > zombieX:
                    if block.getTransform().getPos().getY()-1 < zombieY and block.getTransform().getPos().getY()+2 > zombieY:
                        if block.getTransform().getPos().getZ()-1 < zombieZ and block.getTransform().getPos().getZ()+2 > zombieZ:
                            zombieZ +=0.1
            if self.showbase.zombies[str(id)+"_Isjump"] == True:
                if self.showbase.zombies[str(id)+"_objectif"] > zombieZ:
                    zombieZ += 0.4
                else:
                    self.showbase.zombies[str(id)+"_Isjump"] = False
                        # Récupérer la position du joueur
            playerX = self.showbase.userShape.getTransform().getPos().getX()
            playerY = self.showbase.userShape.getTransform().getPos().getY()

            # Calculer le déplacement du zombie vers le joueur en X et Y
            delta_X = playerX - zombieX
            delta_Y = playerY - zombieY

            # Calculer la nouvelle position du zombie en X et Y
            new_X = zombieX + delta_X * 0.005  # Ajustez la vitesse de déplacement
            new_Y = zombieY + delta_Y * 0.005
            self.showbase.zombies[str(id)+"_zombie"].lookAt(self.showbase.cameraNode)
            self.showbase.zombies[str(id)+"_zombie"].setP(90)
            self.showbase.zombies[str(id)+"_zombie"].setR(0)
            self.showbase.zombies[str(id)+"_zombie"].setH(self.showbase.zombies[str(id)+"_zombie"].getH()+180)
            self.showbase.zombies[str(id)+"_zombieShape"].setTransform(TransformState.makePos(Vec3(new_X, new_Y, zombieZ)))
            return task.cont
        def update_zombie_to_shape(task):
            if self.showbase.zombies[str(id)+"_isAlive"] == False:
                return task.done
            # Récupérez la position du RigidBodyNode
            rigid_body_position = self.showbase.zombies[str(id)+"_zombieShape"].getTransform().getPos()
            rigid_body_position_2 = Vec3(rigid_body_position.x, rigid_body_position.y, rigid_body_position.z+1)
            # Mettez à jour la position du modèle du personnage
            self.showbase.zombies[str(id)+"_zombie"].setPos(rigid_body_position_2)
            self.showbase.enitiys[str(id)+"_zombie"] = {"type": "zombie", "pos": {"x": rigid_body_position.x, "y": rigid_body_position.y, "z": rigid_body_position.z}, "data": {}}
            self.showbase.zombies[str(id)+"_collider"].setPos(rigid_body_position)
            return task.cont
        taskMgr.add(zombie_gravity, "update_gravity")
        taskMgr.add(update_zombie_to_shape, "update_gravity")