from direct.showbase.ShowBase import ShowBase
from threading import Timer  
from panda3d.core import Vec3, NodePath, LineSegs, LPoint3, Camera, OrthographicLens
from panda3d.bullet import BulletWorld
import time
from lib.blocks.break_blocks import Action_Break_Blocks
from lib.user.user_gen import UserGenerator
from lib.action.user_controls import UserMovement
from lib.world.world_gen import setup_world
from lib.action.user_gravity import User_Gravity
from lib.blocks.gen_block import GenBlocks
from lib.action.is_user_death import IsUserDead
from lib.blocks.place_block import Action_Place_Blocks
from lib.files.save_world import World_Saving
from lib.entitys.zombie_spawn import ZombieGen
from lib.entitys.pig_spawn import pigGen

from threading import Lock
import json

from panda3d.core import loadPrcFile

loadPrcFile("config.prc")

print("MinPy Démmarre, Bon jeu!")
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t

class Main(ShowBase):
    def __init__(self):
        print("Création du core 3d")
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -100))  # Gravité
        self.selectedBlockType = 'grass'
        ShowBase.__init__(self)
        self.zombies = {}
        self.zombiesUUID = []
        self.pigs = {}
        self.pigsUUID = []
        self.disableMouse()
        self.worldVars = setup_world(self)
        self.AnPlayerPosX = 5
        self.data_lock = Lock()
        self.ancien_user_gen = 20
        self.AnPlayerPosY = 5
        self.userInventory = []
        self.AnPlayerPosZ = 5
        self.userLife = 18
        print("Lecture du monde")
        f = open("world.json", "r")
        self.JSON_World = json.loads(f.read())
        self.blocks_for_file_simplet = self.JSON_World["blocks"]
        self.enitiys = self.JSON_World["entitys"]
        f.close()
        self.Isjump = False
        self.objectif = 10
        self.LastPosX = 0
        self.LastPosY = 0
        self.TerrainUserX=-5
        self.TerrainUserY=-5
        print("Chargement du terrain")
        self.blocksgenerated = GenBlocks(self)
        print("Création des entités et autres ressources")
        self.deadControl = IsUserDead(self)

        # Initialisation de la fenêtre et de la caméra
        self.user_gen = UserGenerator(self)
        self.zombieGenerator = ZombieGen(self)
        self.pigGenerator = pigGen(self)
        # Génération du monde et des élément
        # Gestion des mouvements et des commandes
        self.user_move = UserMovement(self)
        self.user_gravity = User_Gravity(self)
        self.break_block = Action_Break_Blocks(self)
        self.block_placer = Action_Place_Blocks(self)
        self.world_saving = World_Saving(self)
        # Créez un objet LineSegs pour dessiner la croix
        # Créez une nouvelle région d'affichage (display region)
        dr = self.win.makeDisplayRegion()
        dr.sort = 20

        # Créez une caméra 2D et configurez-la
        myCamera2d = NodePath(Camera('myCam2d'))
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)  # Dimensions de la caméra 2D
        lens.setNearFar(-1000, 1000)  # Plage de rendu
        myCamera2d.node().setLens(lens)

        # Créez un nœud pour le rendu 2D
        myRender2d = NodePath('myRender2d')
        myRender2d.setDepthTest(False)
        myRender2d.setDepthWrite(False)
        myCamera2d.reparentTo(myRender2d)
        dr.setCamera(myCamera2d)
        self.accept("escape", self.world_saving.save_to_file)
        # Créez un objet LineSegs pour dessiner la croix
        croix = LineSegs()
        croix.setColor(1, 0, 0, 1)  # Couleur de la croix (rouge dans cet exemple)

        # Dimensions de la croix
        taille_croix = 0.1

        # Dessinez la ligne horizontale de la croix
        croix.moveTo(-taille_croix, 0, 0)
        croix.drawTo(taille_croix, 0, 0)

        # Créez un nœud Panda3D pour la croix
        croix_node = NodePath(croix.create())
        croix_node.reparentTo(myRender2d)

        # Placez la croix au milieu de l'écran
        croix_node.setPos(LPoint3(0, 0, 0))
        croix2 = LineSegs()
        croix2.setColor(1, 1, 0, 1)  # Couleur de la croix (rouge dans cet exemple)
        croix2.moveTo(0, -taille_croix, 0)
        croix2.drawTo(0, taille_croix, 0)
        # Créez un nœud Panda3D pour la croix
        croix_node2 = NodePath(croix2.create())
        croix_node2.setName("croix_verticale")
        croix_node2.reparentTo(myRender2d)

        # Placez la croix au milieu de l'écran
        croix_node2.setPos(LPoint3(0, 0, 0))
        # Ajouter une tâche pour mettre à jour les mouvements
        print("Inisialisation de la boucle principale")
        def LaterExecution():
            taskMgr.add(self.general_update_loop, "update_movement")
            taskMgr.add(self.gravity_upate_loop, "update_gravity")
            if len(self.enitiys) == 0:
                self.zombieGenerator.spawn(5, 5, 5)
                self.pigGenerator.spawn(5, 5, 5)
            for entityID in self.enitiys:
                entity = self.enitiys[entityID]
                if entity["type"] == "zombie":
                    self.zombieGenerator.spawn(entity["pos"]["x"], entity["pos"]["y"], entity["pos"]["z"], id=entityID.split("_")[0])
        setTimeout(LaterExecution, 1000)



    def general_update_loop(self, task):
        # Vous pouvez gérer les mouvements ici
        self.user_move.update()
        self.user_gravity.update_user_to_shape()
        self.deadControl.update_dead()
        return task.cont
    def gravity_upate_loop(self, task):
        self.user_gravity.is_under_block()
        return task.cont


if __name__ == "__main__":
    app = Main()
    app.run()
