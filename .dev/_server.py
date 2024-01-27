import socket
import threading
import random
import json
import time
import os
import sys
if len(sys.argv) != 2:
    print(f"Usage: {__file__}: <WorldPath>")
    exit()
print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⣷⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠰⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠆⠀⠀⠀
⠀⠀⢸⣷⣦⣈⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⣁⣴⣾⡇⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣷⣦⣄⣉⠛⠻⢿⣿⣿⡿⠟⠛⣉⣠⣴⣾⣿⣿⣿⣿⡇⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡌⢡⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠘⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠃⠀⠀
⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠿⣿⡇⢸⣿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 __  __ _       ____                             
|  \/  (_)_ __ |  _ \ _   _                      
| |\/| | | '_ \| |_) | | | |                     
| |  | | | | | |  __/| |_| |                     
|_|__|_|_|_| |_|_|    \__, |                     
|  _ \  _____   __  __|___/_ _ ____   _____ _ __ 
| | | |/ _ \ \ / / / __|/ _ \ '__\ \ / / _ \ '__|
| |_| |  __/\ V /  \__ \  __/ |   \ V /  __/ |   
|____/ \___| \_/   |___/\___|_|    \_/ \___|_|   
(for help type /help)
""")
f = open(sys.argv[1], "r")
TEXT = f.read()
JSON = json.loads(TEXT)
JSON_World = JSON["lib"]
blocks_for_file_simplet = JSON_World["blocks"]
enitiys = JSON_World["entitys"]
Players = {}
f.close()
def client_is_alive(client_socket, clients, uid):
    while True:
        try:
            # Vérifiez si le client est fermé
            if client_socket._closed:
                print(f"Successfully unregistered Client {uid}")
                client_socket.close()
                del clients[uid]
                break
        except:
            break

# Configurer le serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)
print("[INFO] Serveur en attente de connexions...")
# Liste pour stocker les clients connectés
clients = {}
isReady = []
def Update_Client(client, uid):
    while True:
        if clients[uid][1] == True:
            for i in list(Players.keys()):
                if uid != i:
                    element = Players[i]
                    client.send(("__PLAY__player:"+str(i)+":"+str(element["pos"]["x"])+":"+str(element["pos"]["y"])+":"+str(element["pos"]["z"])+"__PLAY__").encode('utf-8'))
                    time.sleep(0.3)
def secure_entity_control():
    while True:
        if clients:
            random_client_key = random.choice(list(clients.keys()))
            random_client = clients[random_client_key]
            if random_client[1]:
                # Envoyer un message au client choisi pour lui donner le contrôle
                control_message = "0x000001"
                if random_client[1] == True:
                    random_client[0].send(control_message.encode('utf-8'))
                time.sleep(10)
secure_entity_control_thread = threading.Thread(target=secure_entity_control)
secure_entity_control_thread.start()
def createNewBlock(x, y, z, type):
    blocks_for_file_simplet['{"pos": {"x": '+str(x)+', "y": '+str(y)+', "z": '+str(z)+'}}'] = {"pos": {"x": x,"y": y,"z": z}, "type": type, "data": {}}
def create_tree(x,y,z):
    createNewBlock(
                x,
                y,
                z,  # Utilisez la hauteur calculée
                "wood"
    )
    createNewBlock(
                x,
                y,
                z+2,  # Utilisez la hauteur calculée
                "wood"
    )
    createNewBlock(
                x,
                y,
                z+4,  # Utilisez la hauteur calculée
                "wood"
    )
    createNewBlock(
                x,
                y,
                z+6,  # Utilisez la hauteur calculée
                "wood"
    )
    createNewBlock(
                x,
                y,
                z+8,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x+2,
                y,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x-2,
                y,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x,
                y+2,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x,
                y-2,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x-2,
                y+2,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x+2,
                y-2,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x+2,
                y+2,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    createNewBlock(
                x-2,
                y-2,
                z+6,  # Utilisez la hauteur calculée
                "oak"
    )
    
def handle_client(client_socket, clients, uid):
    while True:
            # Recevoir les données du client
            data = client_socket.recv(1024).decode('utf-8')
            # print(data) debug only
            # Traiter les différents types de messages
            if "ready" in data:
                for i in clients:
                    c_client = clients[i]
                    if c_client[1] == True:
                        c_client[0].send(str("newuser:"+str(uid)+":__:").encode("utf-8"))
                clients[uid][1] = True
                for userID in Players:
                    client_socket.send(str("newuser:"+str(userID)+":__:").encode("utf-8"))
                    time.sleep(1)
            elif "sggccet" in data:
                second_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                second_socket.bind(('0.0.0.0', int(data.split("_P_")[1].split("_P_")[0])))
                second_socket.listen(1)
                rport=int(data.split("_P_")[1].split("_P_")[0])
                second_client, second_addr = second_socket.accept()
                tableX=json.loads(data.split("_TX_")[1].split("_TX_")[0])
                tableY=json.loads(data.split("_TY_")[1].split("_TY_")[0])
                i_randint = 0
                i_tree = 0
                for y in tableY:
                    for x in tableX:
                        for z in range(-15, 0):
                            if i_tree == 14:
                                create_tree(x, y, 0)
                            # Calculez la hauteur en utilisant le bruit perlin
                            normalized_height = z
                            type = 'grass' if z == 0 else 'dirt'
                            if int(normalized_height) * 2 < -10:
                                type = "stone"
                            random_number = i_randint
                            if random_number == 1 or random_number == 10 or random_number == 100 or random_number == 111:
                                type = "iron-ore"
                            if random_number == 2 or random_number == 20 or random_number == 20:
                                type = "coal-ore"
                            if random_number == 3 or random_number == 30:
                                type = "diamond-ore"
                            if random_number == 4:
                                type = "obsidian"
                            i_randint+=1
                            i_tree+=1
                            createNewBlock(
                                x,
                                y,
                                int(normalized_height) * 2,  # Utilisez la hauteur calculée
                                type
                            )
                        createNewBlock(
                            x,
                            y,
                            -20,  # Utilisez la hauteur calculée
                            "bedrock"
                        )
                second_client.send(json.dumps({"lib": {"blocks": blocks_for_file_simplet, "entitys": enitiys}, "nlib": { "blocks": {}, "entitys": {} }, "elib": { "blocks": {}, "entitys": {} }, "glib": { "lib": "lib" }}).encode('utf-8'))
                second_client.send("0x000011".encode("utf-8"))
            elif "cblock" in data:
                create_block_event(data)
            elif data.startswith("array"):
                client_socket.send("__#__".encode('utf-8'))
            elif data.startswith("pos"):
                try:
                    Players[uid]["pos"] = json.loads(data.replace("pos ", ""))
                except:
                    pass
            elif "bblock" in data:
                break_block_event(data)
            elif data.startswith("request"):
                client_socket.send(json.dumps({"lib": {"blocks": blocks_for_file_simplet, "entitys": enitiys}, "nlib": { "blocks": {}, "entitys": {} }, "elib": { "blocks": {}, "entitys": {} }, "glib": { "lib": "lib" }}).encode('utf-8'))
                time.sleep(0.5)
                client_socket.send("0x000011".encode('utf-8'))
            elif "get" in data:
                # ICI L'implémentation du second socket pour envoyer la variable TEXT
                # Créer un deuxième socket pour envoyer la variable TEXT
                second_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                second_socket.bind(('0.0.0.0', int(data.split("_X_")[1].split("_X_")[0])))  # Utilisez un autre port, par exemple 5556
                second_socket.listen(1)

                # Attendre la connexion du client pour le deuxième socket
                second_client, second_addr = second_socket.accept()

                # Envoyer la variable TEXT au client du deuxième socket
                second_client.send(json.dumps({"lib": {"blocks": blocks_for_file_simplet, "entitys": enitiys}, "nlib": { "blocks": {}, "entitys": {} }, "elib": { "blocks": {}, "entitys": {} }, "glib": { "lib": "lib" }}).encode('utf-8'))
                second_client.send("0x000011".encode('utf-8'))
                second_client.close()
                second_socket.close()
            if "__hit__" in data:
                hit_entity_event(data)

def create_block_event(data):
    info_data = str(data.split("_IFO_DAT_")[1].split("_IFO_DAT_")[0])
    try:
        createNewBlock(int(info_data.split("_CBX_")[1].split("_CBX_")[0].split(".")[0]),int(info_data.split("_CBY_")[1].split("_CBY_")[0].split(".")[0]),int(info_data.split("_CBZ_")[1].split("_CBZ_")[0].split(".")[0]),str(info_data.split("_CBT_")[1].split("_CBT_")[0]))
    except KeyError:
        pass
    for s_client in clients:
        clients[s_client][0].send(("cblock:_IFO_DAT_"+str(info_data)+"_IFO_DAT_").encode("utf-8"))
def break_block_event(data):
    info_data = str(data.split("_IFO_DAT_")[1].split("_IFO_DAT_")[0])
    try:
        del blocks_for_file_simplet['{"pos": {"x": '+str(info_data.split("_CBX_")[1].split("_CBX_")[0])+', "y": '+str(info_data.split("_CBY_")[1].split("_CBY_")[0])+', "z": '+str(info_data.split("_CBZ_")[1].split("_CBZ_")[0])+'}}']
    except KeyError:
        pass
    for s_client in clients:
        clients[s_client][0].send(("bblock:_IFO_DAT_"+str(info_data)+"_IFO_DAT_").encode("utf-8"))
def hit_entity_event(data):

    Players[int(data.split("__hit__")[1].split("__hit__")[0])]["data"]["life"] -= 1
    life = Players[int(data.split("__hit__")[1].split("__hit__")[0])]["data"]["life"]
    id = data.split("__hit__")[1].split("__hit__")[0]
    if life < 1:
        clients[int(data.split("__hit__")[1].split("__hit__")[0])][0].send("DEAD".encode("utf-8"))
    print(f"Life of {id}: {life}")

def T_SING():
    while True:
        try:
            command = input("Command: ")
            if command == "/stop":
                print("[INFO] STOPPING SERVER")
                f = open(sys.argv[1], "w")
                f.write(json.dumps({"lib": {"blocks": blocks_for_file_simplet, "entitys": enitiys}, "nlib": { "blocks": {}, "entitys": {} }, "elib": { "blocks": {}, "entitys": {} }, "glib": { "lib": "lib" }}))
                f.close()
                os._exit(0)
            if command == "/help":
                print("""
MINPY DEV SERVER HELP
COMMANDS: /stop, stop the server
/help, this help
CONNECT TO THE SERVER.
Follow instructions at: https://github.com/ATLAbanana35/MinPy
Issues: https://github.com/ATLAbanana35/MinPy/issues
Thanks for using MinPy Dev Server
""")
        except (KeyboardInterrupt, EOFError):
            print("\n[INFO] STOPPING SERVER")
            f = open(sys.argv[1], "w")
            f.write(json.dumps({"lib": {"blocks": blocks_for_file_simplet, "entitys": enitiys}, "nlib": { "blocks": {}, "entitys": {} }, "elib": { "blocks": {}, "entitys": {} }, "glib": { "lib": "lib" }}))
            f.close()
            os._exit(0)
_T_SING = threading.Thread(target=T_SING)
_T_SING.start()
while True:
    # Accepter une connexion
    client, addr = server.accept()
    print(f"[INFO] Connexion établie avec {addr}")
    uid = random.randint(1, 1000)
    # Ajouter le client à la liste
    clients[uid] = [client, False]
    if enitiys.get(uid) == None:
        Players[uid] = {
        "type": "user",
        "pos": {
            "x": 1,
            "y": 1,
            "z": 5
        },
        "data": {
            "inventory": {},
            "life": 18,
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
        Players[uid] = enitiys.get(uid)
    isReady.append(False)
    # Démarrer un thread pour gérer le client
    client_handler = threading.Thread(target=handle_client, args=(client, clients, uid))
    isAliveThread = threading.Thread(target=client_is_alive, args=(client, clients, uid))
    isAliveThread.start()
    updateClient = threading.Thread(target=Update_Client, args=(client,uid))
    updateClient.start()
    client_handler.start()