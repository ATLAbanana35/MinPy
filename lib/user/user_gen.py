from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Point3, Vec3, TransformState
from direct.showbase.ShowBase import ShowBase
class UserGenerator(ShowBase):
    def __init__(self, showbase):
        # Charger le modèle de personnage
        showbase.character = showbase.loader.loadModel("ressources/3d/models/steve/source/steve.fbx")
        showbase.character.reparentTo(showbase.render)
        showbase.character.setScale(0.1, 0.1, 0.1)
        showbase.character.setHpr(0, 90, 0)

        # Créer une forme de capsule pour le personnage
        capsule_shape = BulletBoxShape(Vec3(1, 1, 4))

        # Créer un nœud RigidBody pour le personnage
        character_node = BulletRigidBodyNode("character")
        character_node.addShape(capsule_shape)
        character_node.setMass(10.0)  # Masse du personnage
        character_node.setLinearFactor((0, 0, 1))  # Désactive les mouvements verticaux
        character_node.setAngularFactor((0, 0, 0))  # Désactive la rotation
        character_np = showbase.render.attachNewNode(character_node)
        showbase.world.attachRigidBody(character_node)
        showbase.userShape = character_node
        # Définir la position initiale du personnage
        character_np.setPos(Point3(10, 10, 5))
        showbase.userShape.setTransform(TransformState.makePos(Point3(10, 10, 5)))
        # Variables de gravité
        
        # Démarrer la boucle de mise à jour physique
        
        # Enfin, montrez le modèle de personnage
        showbase.character.hide()