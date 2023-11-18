from direct.showbase.ShowBase import ShowBase
from threading import Timer  
from panda3d.core import Vec3, NodePath, LineSegs, LPoint3, Camera, OrthographicLens
from panda3d.bullet import BulletWorld

import time
from threading import Lock
import json
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
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
from lib.user.user_inventory import UserInventory
from lib.gui.open_gui import GUI_OPENING
from lib.action.sound import Sound

from panda3d.core import loadPrcFile

loadPrcFile("config.prc")

print("MinPy Démmarre, Bon jeu!")
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t

class Main(ShowBase):
    def __init__(self):
        self.current_sound_walk = None
        self.is_breaking_block = False
        self.witch_block = None
        self.break_progress = None
        self.break_timer = None
        self.block_to_break = None
        self.time_to_break = 2
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
        self.isGUIopen = False
        self.AnPlayerPosZ = 5
        self.userLife = 18
        # Ressources extractor
        self.mod_blocks_loaded = {}
        self.userInventory = {}
        self.mod_items_loaded = {}
        print("Lecture des ressources")
        f = open("ressources/pycraft/blocks.json", "r")
        self.mods_blocks = json.loads(f.read())
        for index in self.mods_blocks:
            element = self.mods_blocks[index]
            self.mod_blocks_loaded[element["id"]] = loader.loadModel(element["model_path"])
        f = open("ressources/pycraft/gui.json", "r")
        self.mods_guis = json.loads(f.read())
        f = open("ressources/pycraft/items.json", "r")
        self.mods_items = json.loads(f.read())
        index_for_inventory = 0
        for index in self.mods_items:
            element = self.mods_items[index]
            # self.userInventory[index_for_inventory] = [self.mods_items[index], 1]
            index_for_inventory += 1
        print("Lecture du monde")
        f = open("world.json", "r")
        self.JSON_World = json.loads(f.read())
        self.blocks_for_file_simplet = self.JSON_World["blocks"]
        self.enitiys = self.JSON_World["entitys"]
        self.TerrainUserX=-5
        self.TerrainUserY=-5
        self.LastPosX = 0
        self.LastPosY = 0
        if self.enitiys.get("User") == None:
            self.enitiys["User"] = {
    "type": "user",
      "pos": {
        "x": 1,
        "y": 1,
        "z": 5
      },
      "data": {
          "inventory": self.userInventory
      }
      }
        else:
            self.userInventory = self.enitiys.get("User")["data"]["inventory"]
            if int(self.enitiys.get("User")["pos"]["x"]) > -20 and int(self.enitiys.get("User")["pos"]["y"]) > -20 and int(self.enitiys.get("User")["pos"]["x"]) < 20 and int(self.enitiys.get("User")["pos"]["y"]) < 20:
                print("PLAYER DON'T CHANGE POSITION")
            else:
                self.TerrainUserX=int(self.enitiys.get("User")["pos"]["x"])-5
                self.TerrainUserY=int(self.enitiys.get("User")["pos"]["y"])-5
                self.LastPosX = int(self.enitiys.get("User")["pos"]["x"])
                self.LastPosY = int(self.enitiys.get("User")["pos"]["y"])
        f.close()
        self.Isjump = False
        self.objectif = 10
        self.sound = Sound(self)
        print("Chargement du terrain")
        self.blocksgenerated = GenBlocks(self)
        self.user_inventory = UserInventory(self)
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
        self.gui_instance = GUI_OPENING(self)
        def open_player_gui():
            self.gui_instance.open_craft_gui(self.mods_guis["Player_Inventory"])
        self.accept("e", open_player_gui)
        def delete_object():
            for indexX in self.userInventory:
                element = self.userInventory[indexX]
                if element[0]["id"].replace("Item", "") == self.selectedBlockType:
                    del self.userInventory[indexX]
                    break
        self.accept("q", delete_object)
        # Créez un objet LineSegs pour dessiner la croix
        # Créez une nouvelle région d'affichage (display region)
        self.accept("0", self.world_saving.save_to_file)
        # Ajouter une tâche pour mettre à jour les mouvements
        dr = self.win.makeDisplayRegion()
        dr.sort = 20
        myCamera2d = NodePath(Camera('myCam2d'))
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        myCamera2d.node().setLens(lens)

        myRender2d = NodePath('myRender2d')
        myRender2d.setDepthTest(False)
        myRender2d.setDepthWrite(False)
        myCamera2d.reparentTo(myRender2d)
        dr.setCamera(myCamera2d)
        textObject = OnscreenText(text ='+', pos = (0,0), scale = 0.5)
        imageObject = OnscreenImage(image = 'ressources/image/gui/inventory_bar.png', pos = (0,0,-0.7), scale=Vec3(1, 1, 0.1))
        print("Inisialisation de la boucle principale")
        def LaterExecution():
            taskMgr.add(self.general_update_loop, "update_movement")
            taskMgr.add(self.gravity_upate_loop, "update_gravity")
            # self.user_move.startMouseRotation()
            # self.user_move.startMousePan()
            if len(self.enitiys) == 1:
                self.zombieGenerator.spawn(5, 5, 5)
                self.pigGenerator.spawn(5, 5, 5)
            for entityID in self.enitiys:
                entity = self.enitiys[entityID]
                if entity["type"] == "zombie":
                    self.zombieGenerator.spawn(entity["pos"]["x"], entity["pos"]["y"], entity["pos"]["z"], id=entityID.split("_")[0])
        setTimeout(LaterExecution, 1000)



    def general_update_loop(self, task):
        # Vous pouvez gérer les mouvements ici
        self.user_inventory.refresh()
        self.user_move.update()
        self.user_gravity.update_user_to_shape()
        self.deadControl.update_dead()
        self.break_block.is_clicking()
        return task.cont
    def gravity_upate_loop(self, task):
        self.user_gravity.is_under_block()
        return task.cont


if __name__ == "__main__":
    app = Main()
    app.run()
