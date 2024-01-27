from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Point3, Vec3, TransformState, BitMask32
from panda3d.core import CollisionNode, CollisionBox
import random
from direct.showbase.ShowBase import ShowBase
import uuid
class pigGen(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def spawn(self, x, y, z, id=uuid.uuid4()):
        self.showbase.pigs[str(id)+"_current_direction"] = Vec3(x, y, z)  # Direction initiale
        self.showbase.pigsUUID.append(id)
        self.showbase.pigs[str(id)+"_isAlive"] = True
        self.showbase.pigs[str(id)+"_Isjump"] = False
        self.showbase.pigs[str(id)+"_objectif"] = 10
        # Charger le modèle de personnage
        self.showbase.pigs[str(id)+"_pig"] = self.showbase.loader.loadModel("ressources/3d/models/pig/pig.glb")
        self.showbase.pigs[str(id)+"_pig"].reparentTo(self.showbase.render)
        self.showbase.pigs[str(id)+"_pig"].setScale(0.1, 0.1, 0.1)
        self.showbase.pigs[str(id)+"_pig"].setHpr(0, 45, 0)

        # Créer une forme de capsule pour le personnage
        capsule_shape = BulletBoxShape(Vec3(2, 2, 4))

        # Créer un nœud RigidBody pour le personnage
        pig_node = BulletRigidBodyNode("pig")
        pig_node.addShape(capsule_shape)
        pig_node.setMass(10.0)  # Masse du personnage
        self.showbase.pigs[str(id)+"_collider"] = self.showbase.pigs[str(id)+"_pig"].attachNewNode(pig_node)
        self.showbase.pigs[str(id)+"_collider"].setPythonTag('owner', pig_node)
        self.showbase.pigs[str(id)+"_collider"].setCollideMask(BitMask32.allOn())  # Activer la collision avec tout
        self.showbase.pigs[str(id)+"_collider"].setPos(5, 5, 0)
        self.showbase.pigs[str(id)+"_collider"].reparentTo(self.showbase.lightNode)
        pig_node.setLinearFactor((0, 0, 1))  # Désactive les mouvements verticaux
        pig_node.setAngularFactor((0, 0, 0))  # Désactive la rotation
        pig_np = self.showbase.render.attachNewNode(pig_node)
        self.showbase.world.attachRigidBody(pig_node)
        self.showbase.pigs[str(id)+"_pigShape"] = pig_node
        self.showbase.pigs[str(id)+"_pig"].setPythonTag("type", "pig")
        self.showbase.pigs[str(id)+"_pig"].setPythonTag("life", 18)
        self.showbase.pigs[str(id)+"_pig"].setPythonTag("id", id)
        # Définir la position initiale du personnage
        pig_np.setPos(Point3(x, y, z))
        self.showbase.pigs[str(id)+"_pigShape"].setTransform(TransformState.makePos(Point3(x, y, z)))
        # Variables de gravité
        pigSolid = CollisionBox((-2, -2, -2), (2, 2, 2))
        pigNode = CollisionNode('pig_'+str(id))
        pigNode.addSolid(pigSolid)
        collider = self.showbase.pigs[str(id)+"_pig"].attachNewNode(pigNode)
        collider.setPythonTag('owner', self.showbase.pigs[str(id)+"_pig"])
        collider.setPythonTag('rigidBody', pig_node)
        # Enfin, montrez le modèle de personnage
        def pig_gravity(task):
            if self.showbase.pigs[str(id)+"_isAlive"] == False:
                return task.done
            pigX = self.showbase.pigs[str(id)+"_pigShape"].getTransform().getPos().getX()
            pigY = self.showbase.pigs[str(id)+"_pigShape"].getTransform().getPos().getY()
            pigZ = self.showbase.pigs[str(id)+"_pigShape"].getTransform().getPos().getZ()
            pigZ -= 0.1

            for blockIndex in self.showbase.blocks:
                block = self.showbase.blocks[blockIndex]
                if block.getTransform().getPos().getX()-1.4 < pigX and block.getTransform().getPos().getX()+1.4 > pigX:
                    if block.getTransform().getPos().getY()-1.4 < pigY and block.getTransform().getPos().getY()+1.4 > pigY:
                        if block.getTransform().getPos().getZ()-1 < pigZ and block.getTransform().getPos().getZ()+0.5 > pigZ:
                            pigZ += 0.5
            for blockIndex in self.showbase.blocks:
                block = self.showbase.blocks[blockIndex]
                if block.getTransform().getPos().getX()-1 < pigX and block.getTransform().getPos().getX()+2 > pigX:
                    if block.getTransform().getPos().getY()-1 < pigY and block.getTransform().getPos().getY()+2 > pigY:
                        if block.getTransform().getPos().getZ()-1 < pigZ and block.getTransform().getPos().getZ()+2 > pigZ:
                            pigZ +=0.1
            if self.showbase.pigs[str(id)+"_Isjump"] == True:
                if self.showbase.pigs[str(id)+"_objectif"] > pigZ:
                    pigZ += 0.4
                else:
                    self.showbase.pigs[str(id)+"_Isjump"] = False
                        # Récupérer la position du joueur

            # Si le pig atteint sa destination, choisissez une nouvelle direction aléatoire
            if random.random() < 0.0005:  # Changer de direction avec une probabilité de 5%
                new_direction = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
                new_direction.normalize()
                self.showbase.pigs[str(id)+"_current_direction"] = new_direction

            # Calculer la nouvelle position du pig en X et Y en fonction de sa direction actuelle
            new_X = pigX + self.showbase.pigs[str(id)+"_current_direction"].getX() * 0.001
            new_Y = pigY + self.showbase.pigs[str(id)+"_current_direction"].getY() * 0.001

            self.showbase.pigs[str(id)+"_pig"].lookAt(self.showbase.cameraNode)
            self.showbase.pigs[str(id)+"_pig"].setP(90)
            self.showbase.pigs[str(id)+"_pig"].setR(0)
            self.showbase.pigs[str(id)+"_pig"].setH(self.showbase.pigs[str(id)+"_pig"].getH()+180)
            self.showbase.pigs[str(id)+"_pigShape"].setTransform(TransformState.makePos(Vec3(new_X, new_Y, pigZ)))
            return task.cont
        def update_pig_to_shape(task):
            if self.showbase.pigs[str(id)+"_isAlive"] == False:
                return task.done
            # Récupérez la position du RigidBodyNode
            rigid_body_position = self.showbase.pigs[str(id)+"_pigShape"].getTransform().getPos()
            rigid_body_position_2 = Vec3(rigid_body_position.x, rigid_body_position.y, rigid_body_position.z+1)
            # Mettez à jour la position du modèle du personnage
            self.showbase.pigs[str(id)+"_pig"].setPos(rigid_body_position_2)
            self.showbase.enitiys[str(id)+"_pig"] = {"type": "pig", "pos": {"x": rigid_body_position.x, "y": rigid_body_position.y, "z": rigid_body_position.z}, "data": {}}
            self.showbase.pigs[str(id)+"_collider"].setPos(rigid_body_position)
            return task.cont
        taskMgr.add(pig_gravity, "update_gravity")
        taskMgr.add(update_pig_to_shape, "update_gravity")