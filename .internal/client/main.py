from direct.showbase.ShowBase import ShowBase
from threading import Timer  
from panda3d.core import Vec3, NodePath, LineSegs, Point3, Camera, OrthographicLens, TransformState
from panda3d.bullet import BulletWorld
import math
import time
import os
import sys
import random
from direct.interval.IntervalGlobal import Wait

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
from lib.gui.chat import Chat
from lib.entitys.player import playerGen

from panda3d.core import loadPrcFile
if len(sys.argv) != 2:
    print(f"Usage: {__file__}: <Server IP>")
    exit()
loadPrcFile("config.prc")
print("MinPy Démmarre, Bon jeu!")
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t

import socket
import threading
import time
# Configurer le client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((sys.argv[1], 5555))

# Démarrer un thread pour recevoir les messages du serveur
client_socket = client

def send_data_event(data_type, data):
    # Fonction pour envoyer des données avec un type spécifié
    message = f"{data_type} {data}"
    client.send(message.encode('utf-8'))
print_2 = print
def main():
    class Main(ShowBase):
        def __init__(self):
            os.chdir(os.path.dirname(os.path.realpath(__file__)))

            self.current_sound_walk = None
            self.timeline_control = send_data_event
            self.is_breaking_block = False
            self.witch_block = None
            self.break_progress = None
            self.break_timer = None
            self.block_to_break = None
            self.time_to_break = 2
            self.world = BulletWorld()
            self.world.setGravity(Vec3(0, 0, -100))  # Gravité
            self.selectedBlockType = 'grass'
            ShowBase.__init__(self)
            self.zombies = {}
            self.zombiesUUID = []
            self.players = {}
            self.playersUUID = []
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
            self.chat = Chat(self)
            def print(data):
                self.chat.print(data)
            self.print = print
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
            f = open("ressources/pycraft/quest.json", "r")
            self.quests = json.loads(f.read())
            f.close()
            index_for_inventory = 0
            for index in self.mods_items:
                element = self.mods_items[index]
                # self.userInventory[index_for_inventory] = [self.mods_items[index], 1]
                index_for_inventory += 1
            print("Lecture du monde")
            self.world_uptown = ""
            self.timeline_control("request", "first_connexion")
            received_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                if chunk == b'0x000011':
                    break
                received_data += chunk
            self.world_uptown = received_data.decode("utf-8")
            if self.world_uptown == "":
                print_2("Cannot connect to server or data corrupt.")
                exit()
            self.JSON = json.loads(self.world_uptown)
            self.JSON_World = self.JSON["lib"]
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
            "inventory": self.userInventory,
            "life": self.userLife,
            "quests": {
                "0x00001": False,
                "0x00011": False,
                "0x00111": False,
                "0x01111": False,
                "0x11111": False
            }
        }
        }
            else:
                self.userInventory = self.enitiys.get("User")["data"]["inventory"]
                if int(self.enitiys.get("User")["pos"]["x"]) > -20 and int(self.enitiys.get("User")["pos"]["y"]) > -20 and int(self.enitiys.get("User")["pos"]["x"]) < 20 and int(self.enitiys.get("User")["pos"]["y"]) < 20:
                    pass
                else:
                    self.TerrainUserX=int(self.enitiys.get("User")["pos"]["x"])-5
                    self.TerrainUserY=int(self.enitiys.get("User")["pos"]["y"])-5
                    self.LastPosX = int(self.enitiys.get("User")["pos"]["x"])
                    self.LastPosY = int(self.enitiys.get("User")["pos"]["y"])
                    self.userLife = int(self.enitiys.get("User")["data"]["life"])
            f.close()
            self.Isjump = False
            self.objectif = 10
            self.sound = Sound(self)
            print("Chargement du terrain")
            self.zombieGenerator = ZombieGen(self)
            self.playerGenerator = playerGen(self)
            self.blocksgenerated = GenBlocks(self)
            self.user_inventory = UserInventory(self)
            print("Création des entités et autres ressources")
            self.deadControl = IsUserDead(self)

            # Initialisation de la fenêtre et de la caméra
            self.user_gen = UserGenerator(self)
            self.pigGenerator = pigGen(self)
            # Génération du monde et des élément
            self.isMain = False
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
            self.accept("z", self.gui_instance.open_quest_gui)
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
            self.hearts_text = OnscreenText(text ='000000000', pos = (-0.4,-0.55), scale = 0.2)
            imageObject = OnscreenImage(image = 'ressources/image/gui/inventory_bar.png', pos = (0,0,-0.7), scale=Vec3(1, 1, 0.1))
            self.timeline_control("ready", "status:ready")
            print("Inisialisation de la boucle principale")

            def LaterExecution():
                taskMgr.add(self.general_update_loop, "update_movement")
                taskMgr.add(self.gravity_upate_loop, "update_gravity")
                taskMgr.add(self.client_background, "client_background")
                
                
                # self.user_move.startMouseRotation()
                # self.user_move.startMousePan()
                self.playerGenerator.spawn(self.LastPosX, self.LastPosY, 5, id="00000000")
                # for entityID in self.enitiys:
                #     entity = self.enitiys[entityID]
                #     if entity["type"] == "zombie":
                #         self.zombieGenerator.spawn(entity["pos"]["x"], entity["pos"]["y"], entity["pos"]["z"], id=entityID.split("_")[0])
                
                
            setTimeout(LaterExecution, 1000)
            isAliveThread = threading.Thread(target=self.vc)
            isAliveThread.start()
        async def client_background(self, task):
            send_data_event("array", json.dumps(self.enitiys.get("User")["data"]))
            send_data_event("pos", json.dumps(self.enitiys.get("User")["pos"]))
            await Wait(0.2)
            return task.cont
        def vc(self):
            while True:
                try:
                    random_port = random.randint(6000, 9999)
                    self.timeline_control("get", "_X_"+str(random_port)+"_X_")
                    # Code côté client pour se connecter au deuxième socket
                    second_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    second_client.connect(('127.0.0.1', random_port))  # Assurez-vous de mettre la bonne adresse du serveur

                    # Fermer la connexion du deuxième socket côté client
                    self.world_uptown = ""
                    received_data = b""
                    while True:
                        chunk = second_client.recv(1024)
                        if not chunk:
                            break
                        if chunk == b'0x000011':
                            break
                        received_data += chunk
                    self.world_uptown = received_data.decode("utf-8")
                    if self.world_uptown == "":
                        print_2("Cannot connect to server or data corrupt.")
                    self.JSON = json.loads(self.world_uptown)
                    self.JSON_World = self.JSON["lib"]
                    self.blocks_for_file_simplet = self.JSON_World["blocks"]
                except:
                    pass
                data = client.recv(1024)
                if "newuser:" in data.decode("utf-8"):
                    self.playerGenerator.spawn(self.LastPosX, self.LastPosY, 5, id=data.decode('utf-8').split("newuser:")[1].split(":__:")[0])
                if "DEAD" in data.decode("utf-8"):
                    self.print('Vous avez été tué(e) par "player"')
                    self.userShape.setTransform(TransformState.makePos(Point3(1, 1, 5)))
                    self.blocksgenerated.generateTerrain()
                if "cblock" in data.decode("utf-8"):
                    info_data = str(data.decode("utf-8").split("_IFO_DAT_")[1].split("_IFO_DAT_")[0])
                    self.createNewBlock(int(info_data.split("_CBX_")[1].split("_CBX_")[0].split(".")[0]),int(info_data.split("_CBY_")[1].split("_CBY_")[0].split(".")[0]),int(info_data.split("_CBZ_")[1].split("_CBZ_")[0].split(".")[0]),str(info_data.split("_CBT_")[1].split("_CBT_")[0]))
                    self.sound.play("default-place-block.mp3", Point3(int(info_data.split("_CBX_")[1].split("_CBX_")[0].split(".")[0]),int(info_data.split("_CBY_")[1].split("_CBY_")[0].split(".")[0]),int(info_data.split("_CBZ_")[1].split("_CBZ_")[0].split(".")[0])))
                if "bblock" in data.decode("utf-8"):
                    info_data = str(data.decode("utf-8").split("_IFO_DAT_")[1].split("_IFO_DAT_")[0])
                    name = 'block-collision-node_'+str(info_data.split("_CBX_")[1].split("_CBX_")[0].split(".")[0])+"_"+str(info_data.split("_CBY_")[1].split("_CBY_")[0].split(".")[0])+"_"+str(info_data.split("_CBZ_")[1].split("_CBZ_")[0].split(".")[0])
                    NodePath = render.find(name)
                    if not NodePath.isEmpty():
                        # Utilisez nodePathTrouve comme nécessaire
                        NodePath.clearPythonTag('owner')
                        NodePath.removeNode()

                        self.world.removeRigidBody(self.blocks[name])
                        del self.blocks[name]

                    else:
                        print("ERROR_SYSTEM_NOT_FATAL", name)
                    self.sound.play("default-place-block.mp3", Point3(int(info_data.split("_CBX_")[1].split("_CBX_")[0].split(".")[0]),int(info_data.split("_CBY_")[1].split("_CBY_")[0].split(".")[0]),int(info_data.split("_CBZ_")[1].split("_CBZ_")[0].split(".")[0])))
                if "__PLAY__" in data.decode("utf-8"):
                    # try:
                        if data.decode("utf-8").split("__PLAY__")[1].split("__PLAY__")[0] != None:
                            if self.players.get(str(data.decode("utf-8").split(":")[1])+"_playerShape") != None:
                                data2 = data.decode("utf-8").split("__PLAY__")[1].split("__PLAY__")[0]
                                self.players[str(data2.split(":")[1])+"_playerShape"].setTransform(TransformState.makePos(Vec3(float(data2.split(":")[2]), float(data2.split(":")[3]), float(data2.split(":")[4]))))
                    # except:
                    #     pass
        def general_update_loop(self, task):
            self.chat.update()
            self.user_inventory.refresh()
            self.user_move.update()
            self.user_gravity.update_user_to_shape()
            self.deadControl.update_dead()
            self.break_block.is_clicking()
            text = ""
            for i in range(math.floor(self.userLife/2)):
                text += "0"
            self.hearts_text.text = text
            return task.cont
        def gravity_upate_loop(self, task):
            self.user_gravity.is_under_block()
            return task.cont


    if __name__ == "__main__":
        print("Création du core 3d")
        app = Main()
        app.run()

if __name__ == "__main__":
    main()
